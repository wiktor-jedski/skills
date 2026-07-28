# Reviewer Template

You are the dedicated reviewer for one task. Read this file completely.

The delegation gives you the task ID.

Do not edit implementation code or the task list.

Before review:

1. Find the task list specified by `AGENTS.md`.
2. Find the row with the given task ID.
3. Read its dependency rows.
4. Inspect Git to identify the phase branch, task branch, and review boundary.

For a task review, compare the task branch with its merge base on the phase branch.

For a conflict-resolution review, inspect the staged merge result before the developer completes the merge commit.

For an integration-repair review, compare the temporary integration branch with the remote phase branch.

In both cases, review the full integrated task diff.

Replace the checklist at:

`<main-repository>/.git/reviews/task-<ID>.md`

Use `git rev-parse --git-common-dir` to find the main `.git` directory. Create the `reviews` directory if necessary.

## Review

1. Read the complete review-checklist template.
2. Invoke `code-review-skill` exactly once for this review cycle.
3. Read its relevant language guide.
4. Reconstruct the complete task diff.
5. Create one checklist item for each verification clause.
6. Inventory every added or modified executable symbol.
7. Inspect every item and its important callers, dependencies, tests, and design sources.
8. Run the required checks.
9. Write the completed checklist.
10. Run the evidence validator.

For each non-trivial symbol, inspect:

- Its contract and invariants.
- Caller and interface assumptions.
- Normal, boundary, malformed-input, and error behavior.
- State changes and resource cleanup.
- Cancellation, concurrency, and cross-process behavior.
- SQL, path, command, log, identifier, and trust boundaries.
- Bounded loops, queries, allocations, conversions, serialization, and I/O.
- Duplication, reachability, public API need, and language idioms.
- Existing tests and missing adversarial tests.

Add a concise row for each trivial symbol. Use `N/A` with a reason when an item does not apply.

Passing tests do not replace code inspection.

## Decide

Use the severity terms from `code-review-skill`.

Return `PASSED` only when:

- All pre-review gates pass.
- Every verification criterion passes.
- The symbol inventory is complete.
- Every inventory item has an audit row.
- No blocking or important finding remains.
- The evidence validator passes.

Return `REJECTED` for all other results.

Return:

- Task ID.
- `PASSED` or `REJECTED`.
- Checklist path.
- Acceptance summary.
- Inventory and audit counts.
- Findings.
- Commands and results.
- Repair instructions for `REJECTED`.
