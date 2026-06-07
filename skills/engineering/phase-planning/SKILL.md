---
name: phase-planning
description: Plan or refine Mealswapp implementation phases from repository planning docs. Use when Codex is asked to start a phase, plan a phase, expand docs/implementation/01_PLAN.md into docs/implementation/02_TASK_LIST.md, add phase tasks, map work to docs/design static aspects, define dependencies, add verification criteria, or record missing design assumptions in docs/implementation/04_OPEN.md.
---

# Phase Planning

## Overview

Turn the phase-level implementation plan into an actionable, traceable task list. Keep planning changes scoped to `docs/implementation/02_TASK_LIST.md` and `docs/implementation/04_OPEN.md` unless the user explicitly asks for broader edits.

## Workflow

1. Identify the target phase from the user request. If omitted, infer the next phase from the highest fully `PASSED` phase in `docs/implementation/02_TASK_LIST.md` and `docs/implementation/01_PLAN.md`.
2. Read `docs/implementation/01_PLAN.md`, current `docs/implementation/02_TASK_LIST.md`, and the design files named by the target phase.
3. If task-list format, status vocabulary, or open-item conventions are unclear, read `references/mealswapp-task-planning.md`.
4. Generate or update only the target phase rows. Preserve existing task IDs, statuses, retries, and evidence for other phases.
5. Assign monotonically increasing numeric task IDs. Keep dependencies explicit by task ID and avoid dependency cycles.
6. Map every task to exactly one relevant architecture or design source and static aspect in the `Static Aspect` column, such as `DESIGN-010: RouteHandler` or `ARCH-005: RepositoryInterfaces`.
7. Write verification criteria as concrete pass/fail evidence, including commands, API checks, UI checks, data assertions, or document checks as appropriate.
8. Include expected integration, functional, end-to-end, and acceptance coverage in the phase tasks or verification criteria. Put any accepted coverage exception in `Testing Coverage Exceptions`.
9. Add assumptions, clarifications, or project-owner actions to `docs/implementation/04_OPEN.md` only when the design docs do not resolve them.
10. Run `python3 scripts/check.py` when feasible after editing docs. If not feasible, state why.

## Task Design

- Prefer implementation slices that a coder can complete and verify independently.
- Keep tasks ordered by real dependency: data/contracts before services, services before routes, routes before frontend clients, clients before UI workflows, and implementation before UAT documentation.
- Include test-building tasks near the behavior they verify, not as a single end-of-phase cleanup task.
- Use `OPEN` for planned tasks. Do not mark tasks `PREPARED` or `PASSED` during planning unless the user supplies current evidence.
- Keep descriptions phase-prefixed, for example `Phase 02: add versioned API route groups...`.
- Do not create tasks that only say "review", "polish", or "cleanup"; attach the concrete artifact and verification evidence.

## Traceability

- Prefer `DESIGN-*` references when a design file defines the implementation surface.
- Use `ARCH-*` references when the phase plan points to an architecture decision that has no corresponding `DESIGN-*` task surface.
- Verify referenced docs exist before writing the row.
- If a needed static aspect is absent from the design docs, record the assumption or clarification in `docs/implementation/04_OPEN.md` instead of inventing a misleading aspect.

## Output

End with a concise summary of changed files, the target phase planned, and validation run. Mention unresolved open items added to `04_OPEN.md`.
