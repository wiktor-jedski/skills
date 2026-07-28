#!/usr/bin/env python3
"""Validate structural review-evidence gates for phase-orchestrator."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "## 1. Task Source",
    "## 2. Pre-Review Gates",
    "## 3. Review Surface",
    "## 4. Acceptance Criteria",
    "## 5. Changed-Symbol Inventory",
    "## 6. Function-Level Audit",
    "## 7. Findings",
    "## 8. Commands Run",
    "## 9. Coverage and Exceptions",
    "## 10. Negative and Regression Checks",
    "## 11. Decision",
]


def scalar(text: str, key: str) -> str | None:
    matches = re.findall(rf'(?m)^{re.escape(key)}:\s*["\']?([^"\'\n]+)', text)
    return matches[-1].strip() if matches else None


def boolean(text: str, key: str) -> bool | None:
    value = scalar(text, key)
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def integer(text: str, key: str) -> int | None:
    value = scalar(text, key)
    if value is None or not value.isdigit():
        return None
    return int(value)


def section(text: str, heading: str, next_heading: str) -> str:
    start = text.find(heading)
    end = text.find(next_heading, start + len(heading))
    if start < 0 or end < 0:
        return ""
    return text[start + len(heading) : end]


def table_row_count(section_text: str) -> int:
    rows = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        if re.fullmatch(r"[|:\-\s]+", stripped):
            continue
        rows.append(stripped)
    return max(0, len(rows) - 1)  # exclude the header row


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"missing required heading: {heading}")
    if re.search(r"{{[^{}]+}}", text):
        errors.append("unresolved template placeholders remain")

    if integer(text, "task_id") is None:
        errors.append("task_id must be a non-negative integer")
    decision = scalar(text, "decision")
    if decision not in {"PASSED", "REJECTED"}:
        errors.append("decision must be PASSED or REJECTED")
    if scalar(text, "review_kind") not in {"TASK", "INTEGRATION"}:
        errors.append("review_kind must be TASK or INTEGRATION")

    source_count = integer(text, "inventory_source_count")
    audited_count = integer(text, "audited_symbol_count")
    inventory_section = section(text, REQUIRED_HEADINGS[4], REQUIRED_HEADINGS[5])
    audit_section = section(text, REQUIRED_HEADINGS[5], REQUIRED_HEADINGS[6])
    inventory_rows = table_row_count(inventory_section)
    audit_rows = table_row_count(audit_section)
    if source_count is None or audited_count is None:
        errors.append("inventory and audit counts must be non-negative integers")
    else:
        if source_count != inventory_rows:
            errors.append(
                f"inventory_source_count={source_count} but inventory table has {inventory_rows} rows"
            )
        if audited_count != audit_rows:
            errors.append(
                f"audited_symbol_count={audited_count} but audit table has {audit_rows} rows"
            )
        if decision == "PASSED" and source_count != audited_count:
            errors.append("PASSED review has unaudited inventory entries")

    for key in ("blocking_findings", "important_findings", "optional_findings"):
        if integer(text, key) is None:
            errors.append(f"{key} must be a non-negative integer")

    if decision == "PASSED":
        required_true = {
            "code_review_skill_invoked": boolean(text, "code_review_skill_invoked"),
            "pre_review_gates_passed": boolean(text, "pre_review_gates_passed"),
            "inventory_complete": boolean(text, "inventory_complete"),
        }
        for key, value in required_true.items():
            if value is not True:
                errors.append(f"PASSED review requires {key}: true")
        if integer(text, "blocking_findings") != 0:
            errors.append("PASSED review cannot have blocking findings")
        if integer(text, "important_findings") != 0:
            errors.append("PASSED review cannot have important findings")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    if not args.evidence.is_file():
        print(f"review evidence does not exist: {args.evidence}", file=sys.stderr)
        return 2
    errors = validate(args.evidence)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Review evidence is structurally valid: {args.evidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
