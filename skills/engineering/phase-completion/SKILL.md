---
name: phase-completion
description: Complete and validate Mealswapp implementation phases after code or documentation work. Use when Codex is asked to finish a phase, validate PASSED tasks, run or request verification scripts, confirm coverage gates, check design traceability comments and JSON sidecar docs, generate docs/implementation/implemented/{phase:02d}_PHASE_UAT.md, or update docs/implementation/04_OPEN.md with assumptions, deviations, or project-owner actions.
---

# Phase Completion

## Overview

Validate that a phase is actually complete before recording completion. Treat task status, UAT documentation, coverage, and traceability as evidence-backed outputs, not administrative cleanup.

## Workflow

1. Identify the target phase from the user request. If omitted, infer the active phase from `docs/implementation/02_TASK_LIST.md` by finding phase rows that are not all `PASSED`.
2. Read `docs/implementation/01_PLAN.md`, `docs/implementation/02_TASK_LIST.md`, `docs/implementation/04_OPEN.md`, `tools.md`, and any existing `docs/implementation/implemented/{phase:02d}_PHASE_UAT.md`.
3. Read the design and architecture files referenced by the target phase tasks.
4. If UAT format or validation expectations are unclear, read `references/mealswapp-phase-completion.md`.
5. For every task already marked `PASSED`, verify that current repository evidence still satisfies its verification criteria.
6. For every task not marked `PASSED`, inspect changed code/docs and run relevant checks before changing status. Do not mark a task `PASSED` from intent alone.
7. Run the strongest feasible validation commands, starting with `python3 scripts/check.py --output docs/implementation/implemented/{phase:02d}_PHASE_REPORT.html`. Add targeted backend, frontend, migration, local stack, traceability, or UAT scripts when relevant and available.
8. Confirm 100% coverage gates or document accepted deviations in `docs/implementation/04_OPEN.md`.
9. Confirm source traceability comments for implemented code and JSON sidecar trace documents. Use the project traceability validator if it exists.
10. Generate or update `docs/implementation/implemented/{phase:02d}_PHASE_UAT.md` with scope, automated verification, project-owner acceptance tests, known notes, and the acceptance decision.
11. Update `docs/implementation/04_OPEN.md` with unresolved assumptions, deviations, and project-owner actions. Remove or mark resolved items only when evidence supports it.
12. Update `docs/implementation/02_TASK_LIST.md` statuses only after validation. Preserve retries unless a retry is part of the current failure/rework history.

## Evidence Rules

- Prefer direct evidence: passing command output, file existence, tests, coverage summaries, route/API responses, screenshots, generated artifacts, and source references.
- If a command cannot run because a local dependency or approval is missing, state the blocked command and keep affected tasks below `PASSED`.
- Do not claim project-owner acceptance tests were performed unless they were actually run in this session or the user supplies explicit evidence.
- Treat `scripts/check.py` as the aggregate coverage gate. Improve or run it; do not invent a separate coverage gate for phase completion.
- Backend `cmd/*` entrypoints may be verified by build or smoke checks when line coverage is intentionally excluded and documented.

## Task Status

- Use `PASSED` only when the task's verification criteria are satisfied by current evidence.
- Use `PREPARED` when implementation appears present but a required validation remains unrun or externally blocked.
- Use `REJECTED` only when the implementation fails the stated criteria and should be reworked.
- Leave `OPEN` for planned but unimplemented tasks.
- Keep dependency order coherent; a task should not be `PASSED` when a hard dependency is failed or missing.

## UAT Document

Create `docs/implementation/implemented/{phase:02d}_PHASE_UAT.md` for each completed phase. Match the existing Phase 00 style unless the repository has adopted a newer format.

Include:

- phase title and scope;
- automated verification commands and expected results;
- project-owner acceptance tests with steps and accept criteria;
- traceability and coverage notes;
- known deviations or actions from `04_OPEN.md`;
- acceptance decision criteria.

## Output

End with changed files, task statuses changed, validation commands run, and any validations not run. Mention whether the phase is ready for project-owner acceptance.
