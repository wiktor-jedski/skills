---
name: phase-planning
description: Plan implementation phases with a task ledger and per-task description and acceptance-criteria files.
disable-model-invocation: true
---

# Phase Planning

Create or refine tasks for one named implementation phase. Keep scheduling
bookkeeping in the task list and implementation detail in one file per task.

## Inputs

The user must name the target phase. Stop if the target phase is missing.

Read the applicable `AGENTS.md` files. Get these items from them:

- Phase plan.
- Task list.
- Open-items document.
- Design and architecture sources.
- Validation command that reads the task list plus `tasks/{ID}.md` files.

Stop and report each missing item. Do not guess a path or command. Treat a
validator that requires descriptions or verification criteria in the task-list
table as incompatible and report it as a blocker before editing.

The task-details directory is `tasks/` beside the task list. For example, a
task list at `docs/implementation/task-list.md` uses
`docs/implementation/tasks/`. Create this directory when it does not exist.

Edit only the task list, task files created or explicitly selected for
refinement, and open-items document unless the user expands the scope.

## Task list

The task table must have at least these columns:

`ID | Architecture Component | Status | Depends On (ID)`

`Architecture Component` contains the identifiers of the architecture
components implemented or changed by the task. Use comma-separated identifiers
when a task spans multiple components. Do not add or infer phase membership in
the task list.

Keep all other bookkeeping columns and the existing table format. Follow
extra-column rules from `AGENTS.md` or the existing table.

Use only these statuses:

- `OPEN`
- `PREPARED`
- `PASSED`

Use growing, unique integer IDs. Use comma-separated task IDs for dependencies.
Use an empty cell when a task has no dependency.

The task list is a ledger. Do not put descriptions, acceptance criteria,
commands, or other implementation detail in it.

## Task files

Store each task's detail in `tasks/{ID}.md`, where `{ID}` exactly matches the
integer in the task list. Use this format:

```md
# Task {ID}

## Description

<Concrete implementation result and relevant design or architecture references.>

## Acceptance Criteria

- <Observable pass or fail outcome, including the relevant test or command.>
```

Do not repeat status, dependencies, or other task-list bookkeeping in a task
file.

## Plan the phase

1. Read the named phase in the phase plan.
2. Extract every exit criterion.
3. Read the existing task-list rows and their task files.
4. Read each design and architecture source named by the phase.
5. Create small implementation slices in dependency order.
6. Map every exit criterion to one or more tasks.

Each task must be implementable and verifiable after its dependencies pass.
Put tests close to the behavior that they verify. Do not create one final
test-cleanup task.

## Write tasks

For each new task:

- Add one task-list row with the relevant `Architecture Component` identifiers,
  `Status` set to `OPEN`, the next available ID, and explicit acyclic
  dependencies.
- Create `tasks/{ID}.md`.
- State one concrete implementation result in `Description`.
- Include all relevant design and architecture references in `Description`.
- Put observable pass or fail evidence in `Acceptance Criteria`.
- Name the relevant tests and commands in `Acceptance Criteria`.

For existing tasks:

- Preserve every existing ID, architecture component, and status.
- Edit an existing task file only when its status is `OPEN` and the user
  explicitly selected that task ID for refinement.
- Keep `PREPARED` and `PASSED` rows and task files unchanged.
- Otherwise, keep existing rows and task files unchanged.

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

Keep each item concrete and tied to implementation risk. Use the source
document as the single source for existing facts.

## Validate

Run the validation command from `AGENTS.md`. It must validate the ledger-only
task-list schema and read `tasks/{ID}.md` for task details.

Planning passes only when:

- Every exit criterion maps to at least one task.
- Every task-list row has exactly one `tasks/{ID}.md` file.
- Every task file has `Description` and `Acceptance Criteria`.
- Every task has valid, acyclic dependencies.
- Every referenced source exists.
- Every task has observable acceptance evidence.
- Every missing design fact is an open item.
- The validation command passes.

If a planning check fails, fix the planning files and run the command again. If
the command cannot run or still requires detail columns in the task list,
report the validator as a blocker; do not restore details to the ledger.

## Report

Report:

- Target phase.
- Changed files.
- Open items added.
- Validation result.
