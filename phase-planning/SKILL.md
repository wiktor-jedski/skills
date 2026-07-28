---
name: phase-planning
description: Plan implementation phases as actionable, traceable task lists.
disable-model-invocation: true
---

# Phase Planning

Create or refine tasks for one named implementation phase.

## Inputs

The user must name the target phase. Stop if the target phase is missing.

Read the applicable `AGENTS.md` files. Get these items from them:

- Phase plan.
- Task list.
- Open-items document.
- Design and architecture sources.
- Validation command.

Stop and report each missing item. Do not guess a path or command.

Edit only the task list and open-items document unless the user expands the scope.

## Task table

The task table must have at least these columns:

`ID | Status | Description | Depends On (ID) | Verification Criteria`

Keep all extra columns and the table format. Follow extra-column rules from `AGENTS.md` or the existing table.

Use only these statuses:

- `OPEN`
- `PREPARED`
- `PASSED`

Use growing, unique integer IDs. Use comma-separated task IDs for dependencies. Use an empty cell when a task has no dependency.

## Plan the phase

1. Read the named phase in the phase plan.
2. Extract every exit criterion.
3. Read the existing tasks for the phase.
4. Read each design and architecture source named by the phase.
5. Create small implementation slices in dependency order.
6. Map every exit criterion to one or more tasks.

Each task must be implementable and verifiable after its dependencies pass.

Put tests close to the behavior that they verify. Do not create one final test-cleanup task.

## Write tasks

For new tasks:

- Set `Status` to `OPEN`.
- Use the next available ID.
- State one concrete implementation result.
- Put all relevant design and architecture references in `Description`.
- Put observable pass or fail evidence in `Verification Criteria`.
- Name the relevant tests and commands in `Verification Criteria`.
- Add explicit dependencies. Keep the dependency graph acyclic.

For existing tasks:

- Preserve every ID and status.
- Edit only `OPEN` tasks in the target phase.
- Keep `PREPARED` and `PASSED` tasks unchanged.
- Keep tasks from other phases unchanged.

Do not repeat the phase name in each description.

## Record open items

Add an open item when:

- A required design or architecture source is missing.
- The sources do not resolve an implementation fact.
- A test type is omitted for a justified reason.
- The project owner must make a decision or take an action.

Use a section for the target phase. Add only headings that contain entries:

- `Assumptions`
- `Clarifications`
- `Actions needed`
- `Testing coverage deviations`

Keep each item concrete and tied to implementation risk. Use the source document as the single source for existing facts.

## Validate

Run the validation command from `AGENTS.md`.

Planning passes only when:

- Every exit criterion maps to at least one task.
- Every task has valid, acyclic dependencies.
- Every referenced source exists.
- Every task has observable verification evidence.
- Every missing design fact is an open item.
- The validation command passes.

If a check fails, fix the planning files and run the command again. Report a blocker when the command cannot run.

## Report

Report:

- Target phase.
- Changed files.
- Open items added.
- Validation result.
