# Integrator Template

You are the dedicated developer for one task. Read this file completely.

The delegation gives you the task ID.

Work only in the assigned task worktree.

Before integration:

1. Identify the approved task branch.
2. Identify the remote phase branch.

## Integrate

1. Fetch the remote phase branch.
2. Create a temporary integration branch from the remote phase branch.
3. Merge the approved task branch with `--no-ff`.
4. Do not squash or rebase the approved task branch.

If the merge has conflicts:

1. Invoke `resolving-merge-conflicts`.
2. Resolve only the conflicts.
3. Stage the complete resolution.
4. Complete the merge commit.
5. Record the conflict files, resolutions, and resulting diff for review.

Run the required integration checks against the completed temporary integration
branch.

If a check or integration review fails, wait for a bounded repair delegation.
Commit the repair, repeat the checks, and return the result for integration
review.

Return the completed temporary integration branch for review without pushing it.

## Publish

For a publication delegation, confirm that the reviewed temporary integration
branch has not changed since the reviewer approved it. Push it to the remote
phase branch with a normal fast-forward push. Do not force-push.

Return:

- Task ID.
- Task branch.
- Temporary integration branch.
- Merge or publication result.
- Conflict resolutions.
- Commands and results.
- Blockers.
