#!/usr/bin/env python3
"""Generate SWE.5 architecture-integration obligation candidates as JSON.

This script is intentionally deterministic. It does not decide final test
scenarios. Instead, it identifies architecture components that are ready for
SWE.5 work and emits enough structured context for an LLM agent to author the
actual Integration Verification Obligation markdown.

Typical use:
    python3 ci/generate_swe5_obligations.py \
      --tasks docs/implementation/tasks.md \
      --code-design docs/design/code-design.md \
      --architecture docs/design/software-architecture.md \
      --tests-root tests \
      --output docs/testing/swe5-obligations.json

Exit codes:
    0  JSON generated successfully.
    2  Required input file is missing or malformed enough to prevent output.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

ARCH_ID_RE = re.compile(r"\bARCH-\d{3}\b")
UNIT_ID_RE = re.compile(r"\bUNIT-\d{3}\b")
REQ_ID_RE = re.compile(r"\bSW-REQ-[A-Za-z0-9]+\b")
ARCH_HEADING_RE = re.compile(r"^##\s+(ARCH-\d{3})\s+-\s+(.+?)\s*$", re.MULTILINE)
UNIT_MATRIX_ROW_RE = re.compile(
    r"^\|\s*`?(UNIT-\d{3})`?\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$"
)
TASK_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|(.+?)\|\s*([A-Z]+)\s*\|\s*(\d+)\s*\|", re.MULTILINE)
TEST_REF_RE = re.compile(r"\b(?:IT[-_]ARCH[-_](\d{3})(?:[-_]\d{3})?|IT[-_](ARCH[-_]\d{3})(?:[-_]\d{3})?)\b", re.IGNORECASE)
VERIFY_REF_RE = re.compile(r"\bVerifies\s+(IT-ARCH-\d{3}-\d{3}|ARCH-\d{3})\b", re.IGNORECASE)


@dataclass(frozen=True)
class TaskRecord:
    id: int
    component: str
    static_aspect: str
    status: str
    arch_ids: list[str]
    unit_ids: list[str]


@dataclass(frozen=True)
class ArchitectureComponent:
    arch_id: str
    name: str
    static_aspects: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    requirement_trace: list[str] = field(default_factory=list)
    dynamic_behavior: list[str] = field(default_factory=list)
    interface_input: str = ""
    interface_output: str = ""


@dataclass(frozen=True)
class TestReference:
    path: str
    line: int
    reference: str
    text: str


def main() -> int:
    args = parse_args()

    try:
        tasks_path = Path(args.tasks)
        code_design_path = Path(args.code_design)
        architecture_path = Path(args.architecture)
        for path in (tasks_path, code_design_path, architecture_path):
            if not path.exists():
                raise ValueError(f"required file not found: {path}")

        tasks = parse_tasks(tasks_path.read_text(encoding="utf-8"))
        unit_to_arch = parse_unit_architecture_mapping(code_design_path.read_text(encoding="utf-8"))
        architecture = parse_architecture(architecture_path.read_text(encoding="utf-8"))
        test_refs = scan_test_references(Path(args.tests_root)) if args.tests_root else []

        payload = build_payload(
            tasks=tasks,
            unit_to_arch=unit_to_arch,
            architecture=architecture,
            test_refs=test_refs,
            implemented_statuses=set(args.implemented_status),
            candidate_arch_statuses=set(args.candidate_arch_status),
            min_implemented_units=args.min_implemented_units,
            source_paths={
                "tasks": str(tasks_path),
                "code_design": str(code_design_path),
                "architecture": str(architecture_path),
                "tests_root": str(Path(args.tests_root)) if args.tests_root else "",
            },
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    text = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)

    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tasks", default="docs/implementation/tasks.md")
    parser.add_argument("--code-design", default="docs/design/code-design.md")
    parser.add_argument("--architecture", default="docs/architecture/software-architecture.md")
    parser.add_argument("--tests-root", default="tests")
    parser.add_argument("--output", default="")
    parser.add_argument(
        "--implemented-status",
        action="append",
        default=["PASSED"],
        help="Task status that counts a UNIT/ARCH item as implemented. Repeatable. Default: PASSED.",
    )
    parser.add_argument(
        "--candidate-arch-status",
        action="append",
        default=["OPEN", "PREPARED"],
        help="Architecture task status that should be flagged as needing SWE.5 planning. Repeatable.",
    )
    parser.add_argument(
        "--min-implemented-units",
        type=int,
        default=2,
        help="Minimum implemented mapped units before an ARCH slice is ready for SWE.5. Default: 2.",
    )
    return parser.parse_args()


def parse_tasks(text: str) -> list[TaskRecord]:
    records: list[TaskRecord] = []
    for line in text.splitlines():
        if not line.startswith("|") or line.startswith("|----") or " Static Aspect " in line:
            continue
        columns = split_markdown_row(line)
        if len(columns) < 5 or not columns[0].isdigit():
            continue
        task_id = int(columns[0])
        component = columns[1].strip()
        static_aspect = columns[2].strip()
        status = columns[3].strip().upper()
        records.append(
            TaskRecord(
                id=task_id,
                component=component,
                static_aspect=static_aspect,
                status=status,
                arch_ids=sorted(set(ARCH_ID_RE.findall(static_aspect))),
                unit_ids=sorted(set(UNIT_ID_RE.findall(static_aspect))),
            )
        )
    return records


def split_markdown_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_unit_architecture_mapping(text: str) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for line in text.splitlines():
        match = UNIT_MATRIX_ROW_RE.match(line)
        if not match:
            continue
        unit_id = match.group(1)
        parent_cell = match.group(3)
        arch_ids = sorted(set(ARCH_ID_RE.findall(parent_cell)))
        if arch_ids:
            mapping[unit_id] = arch_ids
    if not mapping:
        raise ValueError("could not parse any UNIT -> ARCH mappings from code design")
    return mapping


def parse_architecture(text: str) -> dict[str, ArchitectureComponent]:
    matches = list(ARCH_HEADING_RE.finditer(text))
    components: dict[str, ArchitectureComponent] = {}
    for index, match in enumerate(matches):
        arch_id = match.group(1)
        name = match.group(2).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[start:end]
        components[arch_id] = ArchitectureComponent(
            arch_id=arch_id,
            name=name,
            static_aspects=parse_attribute_list(block, "Static Aspects"),
            dependencies=parse_attribute_list(block, "Dependencies"),
            requirement_trace=sorted(set(REQ_ID_RE.findall(parse_attribute_text(block, "Traceability")))),
            dynamic_behavior=parse_dynamic_behavior(block),
            interface_input=parse_interface_line(block, "Input"),
            interface_output=parse_interface_line(block, "Output"),
        )
    if not components:
        raise ValueError("could not parse any ARCH components from architecture document")
    return components


def parse_attribute_text(block: str, attribute: str) -> str:
    pattern = re.compile(rf"^\|\s*\*\*{re.escape(attribute)}\*\*\s*\|\s*(.*?)\s*\|\s*$", re.MULTILINE)
    match = pattern.search(block)
    return strip_markdown(match.group(1)) if match else ""


def parse_attribute_list(block: str, attribute: str) -> list[str]:
    value = parse_attribute_text(block, attribute)
    if not value:
        return []
    parts = [strip_markdown(part.strip()) for part in value.split(",")]
    return [part for part in parts if part]


def parse_dynamic_behavior(block: str) -> list[str]:
    section = extract_section(block, "**Dynamic Behavior:**")
    bullets: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(strip_markdown(stripped[2:].strip()))
    return bullets


def parse_interface_line(block: str, label: str) -> str:
    pattern = re.compile(rf"^-\s*`?{re.escape(label)}`?:\s*(.+?)\s*$", re.MULTILINE)
    match = pattern.search(block)
    return strip_markdown(match.group(1).strip()) if match else ""


def extract_section(block: str, heading: str) -> str:
    start = block.find(heading)
    if start < 0:
        return ""
    tail = block[start + len(heading):]
    next_heading = re.search(r"\n\*\*[A-Za-z ].+?:\*\*", tail)
    if next_heading:
        return tail[: next_heading.start()]
    return tail


def strip_markdown(text: str) -> str:
    return re.sub(r"[`*_]", "", text).strip()


def scan_test_references(root: Path) -> list[TestReference]:
    if not root.exists():
        return []
    refs: list[TestReference] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".cs", ".fs", ".vb", ".py", ".md"}:
            continue
        if any(part in {"bin", "obj", "TestResults"} for part in path.parts):
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, start=1):
            for ref in extract_test_refs_from_line(line):
                refs.append(TestReference(str(path), line_number, normalize_test_ref(ref), line.strip()))
    return refs


def extract_test_refs_from_line(line: str) -> Iterable[str]:
    for match in TEST_REF_RE.finditer(line):
        if match.group(1):
            yield f"ARCH-{match.group(1)}"
        elif match.group(2):
            yield match.group(2).replace("_", "-").upper()
    for match in VERIFY_REF_RE.finditer(line):
        ref = match.group(1).replace("_", "-").upper()
        if ref.startswith("IT-ARCH-"):
            yield ref[:11]
        else:
            yield ref


def normalize_test_ref(ref: str) -> str:
    ref = ref.replace("_", "-").upper()
    match = re.search(r"ARCH-(\d{3})", ref)
    return f"ARCH-{match.group(1)}" if match else ref


def build_payload(
    *,
    tasks: list[TaskRecord],
    unit_to_arch: dict[str, list[str]],
    architecture: dict[str, ArchitectureComponent],
    test_refs: list[TestReference],
    implemented_statuses: set[str],
    candidate_arch_statuses: set[str],
    min_implemented_units: int,
    source_paths: dict[str, str],
) -> dict[str, object]:
    implemented_units = sorted(
        {unit for task in tasks if task.status in implemented_statuses for unit in task.unit_ids}
    )
    implemented_arch_tasks = sorted(
        {arch for task in tasks if task.status in implemented_statuses for arch in task.arch_ids}
    )
    candidate_arch_tasks = sorted(
        {arch for task in tasks if task.status in candidate_arch_statuses for arch in task.arch_ids}
    )

    arch_to_units: dict[str, list[str]] = {}
    for unit_id, arch_ids in unit_to_arch.items():
        for arch_id in arch_ids:
            arch_to_units.setdefault(arch_id, []).append(unit_id)
    for arch_id in arch_to_units:
        arch_to_units[arch_id] = sorted(set(arch_to_units[arch_id]))

    refs_by_arch: dict[str, list[TestReference]] = {}
    for ref in test_refs:
        refs_by_arch.setdefault(ref.reference, []).append(ref)

    components: list[dict[str, object]] = []
    for arch_id in sorted(architecture):
        arch = architecture[arch_id]
        mapped_units = arch_to_units.get(arch_id, [])
        implemented_mapped_units = sorted(set(mapped_units) & set(implemented_units))
        has_enough_units = len(implemented_mapped_units) >= min_implemented_units
        has_implemented_arch_task = arch_id in implemented_arch_tasks
        has_candidate_arch_task = arch_id in candidate_arch_tasks
        existing_refs = refs_by_arch.get(arch_id, [])

        ready = has_enough_units or has_implemented_arch_task or has_candidate_arch_task
        missing_swe5_attention = ready and not existing_refs
        status = (
            "needs_swe5_obligations"
            if missing_swe5_attention
            else "has_swe5_test_references"
            if ready
            else "not_ready"
        )

        components.append(
            {
                "arch_id": arch.arch_id,
                "name": arch.name,
                "status": status,
                "ready_for_swe5": ready,
                "readiness_reasons": readiness_reasons(
                    has_enough_units=has_enough_units,
                    has_implemented_arch_task=has_implemented_arch_task,
                    has_candidate_arch_task=has_candidate_arch_task,
                    min_implemented_units=min_implemented_units,
                ),
                "mapped_units": mapped_units,
                "implemented_units": implemented_mapped_units,
                "static_aspects": arch.static_aspects,
                "architecture_dependencies": arch.dependencies,
                "requirement_trace": arch.requirement_trace,
                "interface": {
                    "input": arch.interface_input,
                    "output": arch.interface_output,
                },
                "dynamic_behavior": arch.dynamic_behavior,
                "existing_test_references": [asdict(ref) for ref in existing_refs],
                "obligation_seed": build_obligation_seed(arch, implemented_mapped_units),
                "agent_instruction": (
                    "Create or update docs/testing/integration/"
                    f"{arch.arch_id}-obligations.md. Derive final SWE.5 obligations from the "
                    "interface, dynamic behavior, collaborators, failure behavior, and requirement trace. "
                    "Do not simply copy unit-test scenarios; each obligation must cross at least two units "
                    "or architecture components unless it is a launch/runtime smoke boundary."
                ),
            }
        )

    return {
        "schema_version": 1,
        "kind": "swe5_obligation_candidates",
        "source_paths": source_paths,
        "policy": {
            "implemented_statuses": sorted(implemented_statuses),
            "candidate_arch_statuses": sorted(candidate_arch_statuses),
            "min_implemented_units": min_implemented_units,
            "integration_test_reference_convention": [
                "Test names or comments contain IT_ARCH_002, IT-ARCH-002, or Verifies ARCH-002.",
                "Final obligations should use stable IDs such as IT-ARCH-002-001.",
            ],
        },
        "summary": {
            "implemented_units": implemented_units,
            "implemented_arch_task_ids": implemented_arch_tasks,
            "candidate_arch_task_ids": candidate_arch_tasks,
            "ready_arch_count": sum(1 for item in components if item["ready_for_swe5"]),
            "needs_swe5_obligations_count": sum(
                1 for item in components if item["status"] == "needs_swe5_obligations"
            ),
        },
        "architecture_components": components,
    }


def readiness_reasons(
    *,
    has_enough_units: bool,
    has_implemented_arch_task: bool,
    has_candidate_arch_task: bool,
    min_implemented_units: int,
) -> list[str]:
    reasons: list[str] = []
    if has_enough_units:
        reasons.append(f"at least {min_implemented_units} mapped units are implemented")
    if has_implemented_arch_task:
        reasons.append("an implementation task for this architecture ID is implemented")
    if has_candidate_arch_task:
        reasons.append("an OPEN/PREPARED task references this architecture ID")
    return reasons


def build_obligation_seed(arch: ArchitectureComponent, implemented_units: list[str]) -> dict[str, object]:
    seeds: list[dict[str, object]] = []
    for index, behavior in enumerate(arch.dynamic_behavior[:8], start=1):
        seeds.append(
            {
                "candidate_id": f"IT-{arch.arch_id}-{index:03d}",
                "basis": "architecture_dynamic_behavior",
                "source_statement": behavior,
                "recommended_obligation_shape": {
                    "intent": "Verify this behavior across collaborating units/components.",
                    "system_under_test": "Choose the primary runtime unit/controller for the architecture component.",
                    "real_components": implemented_units,
                    "test_doubles_allowed": "Only for external boundaries, file system, engine/runtime, UI, or unavailable units.",
                    "stimulus": "Derive from architecture interface input and detailed-design public APIs.",
                    "expected_evidence": "Observable integrated behavior, ordering, produced contract, state transition, or failure policy.",
                },
            }
        )
    return {
        "note": "These are seeds for an LLM agent, not final obligations. A human or LLM should merge, split, and refine them.",
        "candidate_obligations": seeds,
    }


if __name__ == "__main__":
    raise SystemExit(main())
