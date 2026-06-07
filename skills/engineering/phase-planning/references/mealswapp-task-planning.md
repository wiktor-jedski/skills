# Mealswapp Task Planning Reference

## Inputs

- `docs/implementation/01_PLAN.md`: phase source of truth, target architecture/design areas, phase exit criteria, and expected test categories.
- `docs/implementation/02_TASK_LIST.md`: authoritative task table and status source.
- `docs/implementation/04_OPEN.md`: assumptions, clarifications, actions, and accepted deviations.
- `docs/design/DESIGN-*.md` and `docs/architecture/ARCH-*.md`: traceability sources for static aspects.
- `tools.md`: backlog note that defines Phase Planning skill output.

## Task Table Contract

Use the existing table columns exactly:

`ID | Component | Static Aspect | Status | Retries | Description | Depends On (ID) | Testing Coverage Exceptions | Verification Criteria`

Rules:

- `Status` must be one of `OPEN`, `PREPARED`, `REJECTED`, or `PASSED`.
- `ID` must be a growing unique integer.
- `Retries` starts at `0` for new tasks.
- `Depends On (ID)` uses comma-separated task IDs or stays blank.
- `Testing Coverage Exceptions` is `None` unless there is a specific, documented reason.
- `Verification Criteria` must describe observable evidence, not intent.

## Planning Checklist

For each target phase:

1. Extract the phase summary and exit criteria from `01_PLAN.md`.
2. Identify the source design and architecture files named by that phase.
3. Break work into ordered implementation slices with explicit dependencies.
4. Add tests close to the slices they verify:
   - integration tests for module boundaries, persistence, middleware, API contracts, and local services;
   - functional tests for domain behavior and user-visible rules;
   - end-to-end tests for completed user workflows when the phase exposes one;
   - acceptance/UAT tasks or verification criteria that a project owner can perform.
5. Add traceability by choosing one static aspect per row.
6. Record missing design facts in `04_OPEN.md`.

## Open Items

Add a `## Phase NN` section only when there is something useful to record. Prefer these headings:

- `### Assumptions`
- `### Clarifications`
- `### Actions needed`
- `### Testing coverage deviations`

Keep entries concrete and tied to future implementation risk. Do not duplicate information already present in design docs or the task list.
