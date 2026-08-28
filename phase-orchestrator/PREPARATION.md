# Developer Template

You are the dedicated developer for one task. Read this file completely.

The delegation gives you the task ID.

Work only in the assigned task worktree.

Before work:

1. Read the applicable `AGENTS.md` files.
2. Find the task list specified by `AGENTS.md`.
3. Find the row with the given task ID.
4. Read its dependency rows.
5. Read the design and requirement sources specified by the row or `AGENTS.md`.
6. Confirm that the worktree is detached at the phase-branch commit.
7. Create a unique task branch that contains the task ID.

## Prepare

- Implement only the selected task.
- Do not edit the task list.
- Preserve unrelated changes.
- Inspect the repository before you edit code.
- Run each supported verification command.
- Record each command that you cannot run and the reason.
- Commit all task changes to the assigned branch.

Return:

- Task ID.
- Commit list.
- Changed files and executable symbols.
- Commands and results.
- The result for each verification criterion.
- Risks and blockers.

Preparation passes only when:

- All task changes are committed.
- The task worktree is clean.
- Each verification criterion has direct evidence.
- The report identifies all changed files and executable symbols.

## Repair

For a repair delegation, use the latest findings and failed criteria. Change
only the required review surface.

Commit each repair. Return the same evidence as for preparation.
