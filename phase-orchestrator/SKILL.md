---
name: phase-orchestrator
description: Orchestrate implementation, review, and integration of phase tasks.
disable-model-invocation: true
---

# Phase Orchestrator

Process tasks in isolated Git worktrees.

## Inputs

Use the task list specified by the applicable `AGENTS.md`. Use another task list only when the user specifies it.

The table must contain:

`ID | Status | Description | Depends On (ID) | Verification Criteria`

Valid statuses are `OPEN`, `PREPARED`, and `PASSED`.

## Agents

Resolve the absolute path of this skill directory.

For each task, create:

- One developer.
- One reviewer.

Put the applicable template into each subagent's context. In the initial delegation, give only the task ID and the absolute template path:

- Developer: `<skill-directory>/PREPARATION.md`
- Reviewer: `<skill-directory>/REVIEW.md`
- Integrator: `<skill-directory>/INTEGRATION.md`

Use this initial instruction:

```text
Read <absolute-template-path> completely. Follow it as your role template. Do not start the task before you read it.
Task ID: <ID>
```

The subagent gets all other context from `AGENTS.md`, the task list, and Git. The subagent reads and performs the template instructions. The orchestrator must not perform them.

Reuse the same developer and reviewer for all cycles of that task.

Use this communication policy:

- Send one complete delegation when you start an agent.
- While the agent is active, send no messages to it.
- Respond only if the agent asks a question or reports a blocker that needs orchestration input.
- After the agent finishes, a new bounded delegation may request missing evidence or repairs.
- Stop an agent only when the user cancels the work.

## Rules

- Work only in a Git repository.
- Start only when the phase worktree is clean.
- The orchestrator owns the task list. Other agents must not edit it.
- Change only the selected status cell. Preserve all other cells and table format.
- The orchestrator must not implement, review, or integrate task code.
- Integrate one task at a time.
- Keep each merged task branch.
- Remove each task worktree and temporary integration branch after the task passes.

## Process

### 1. Select

Parse task IDs as integers. Treat `-` and an empty dependency cell as no dependencies.

Stop if an ID is not unique, a dependency is missing, or a status is invalid.

An `OPEN` task is eligible only when all its dependencies are `PASSED`.

Sort eligible tasks by ID. Select the smallest ID first.

You may process tasks concurrently when the tasks do not depend on each other.

If no task is eligible, report each blocked task and its unmet dependencies.

### 2. Prepare

Create a detached worktree in `../worktrees/<project-name>/<task-id>/` from the current phase-branch commit. The developer creates the task branch in that worktree.

When preparation passes, change the task from `OPEN` to `PREPARED`. Commit and push this task-list change on the phase branch.

### 3. Review

Delegate review to the task reviewer.

If the result is `REJECTED`, keep the task `PREPARED`. Delegate the repairs to the same developer. Then delegate review to the same reviewer.

Continue until review passes or the user cancels the work.

### 4. Integrate

Delegate integration to the same developer. Use initial instruction with integrator template.

If the merge has conflicts, the developer resolves and stages them. Delegate an integration review to the same reviewer before the developer completes the merge commit.

If an integration check fails, delegate repair to the developer and a full integration review to the reviewer.

Continue repair and review with the same agents until integration passes or the user cancels the work.

The developer pushes the integration result to the remote phase branch.

### 5. Complete

After integration passes:

0. Run `git pull --ff-only`.
1. Change the task from `PREPARED` to `PASSED`.
2. Commit and push this task-list change on the phase branch.
3. Remove the task worktree.
4. Remove the temporary integration branch.
5. Keep the merged task branch.
6. Close the task developer and reviewer.

Create each later worktree from the updated local phase branch.

For one requested task, stop after this step. For all actionable tasks, return to selection.

Report only:

- Task IDs that changed.
- Open or blocked tasks, if any.
