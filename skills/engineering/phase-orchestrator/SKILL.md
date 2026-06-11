---
name: phase-orchestrator
description: MUST use this skill when asked to process a Markdown task table by delegating each OPEN task to a separate OpenCode subagent, waiting for completion, and changing only successful task rows from OPEN to PREPARED.
---

# Phase Orchestrator

Use this skill to implement a workflow for a Markdown task list without context compaction. 
The parent agent is only an orchestrator. Actual task preparation is performed by subagents, 
one task at a time, to avoid edit conflicts.

## Inputs

- Task list path: default `tasks.md` unless the user names another file.
- Target status transition: `OPEN` -> `PREPARED`.
- Valid statuses are `OPEN`, `PREPARED`, `REJECTED`, and `PASSED`.
- A task is eligible only if:
  - its `Status` is exactly `OPEN`;
  - every ID in `Depends On (ID)` is already `PASSED` or `PREPARED`;
  - it has the smallest eligible task ID among remaining `OPEN` tasks.

## Hard rules

1. Run more than one implementation/preparation subagents at the same time if the tasks do not overlap (different files changed, not dependent on each other)
2. For each eligible task, invoke exactly one fresh subagent session and wait for its result before touching the task list.
3. The parent agent must not implement the task itself unless subagent invocation is unavailable. If subagent invocation is unavailable, stop and report the missing Task/subagent capability instead of continuing in the parent context.
4. Do not compact or summarize project context into the parent. Give the subagent only the selected task row, dependency rows needed for context, relevant repository paths it should inspect, and the verification criteria.
5. Do not mark a task `PREPARED` just because work started. Only update the task list after the subagent reports completion and provides evidence matching the verification criteria.
6. Update only the `Status` cell for the selected task row from `OPEN` to `PREPARED` or `REJECTED`. Preserve all other columns and formatting as much as possible.
7. If the subagent reports that the task cannot be completed, leave the row as `OPEN` unless the user explicitly wants failures marked `REJECTED`.
8. Before ending, report which task IDs were changed and which remain blocked/open.

## Procedure

### 1. Read and validate the task table

- Open the task list file.
- Confirm it has these columns: `ID`, `Component`, `Static Aspect`, `Status`, `Retries`, `Description`, `Depends On (ID)`, `Testing Coverage Exceptions`, `Verification Criteria`.
- Parse task IDs as integers.
- Treat `-` or an empty dependency cell as no dependencies.
- Abort if duplicate IDs exist or if a dependency references a missing ID.

### 2. Select the next task

- Find all rows with `Status == OPEN`.
- Filter to rows whose dependencies are all `PASSED` or `PREPARED`.
- Sort eligible rows by numeric `ID`.
- Select the smallest ID.
- If no eligible `OPEN` task exists, report that there is nothing currently actionable and list blocked task IDs with their unmet dependencies.

### 3. Delegate to a subagent

Invoke a writable implementation subagent such as `general` or a project-specific task-preparer subagent. The prompt must include this exact contract:

```text
You are a task-preparation subagent. Prepare exactly one task from the Markdown task list.

Task row:
<copy the full selected Markdown table row>

Dependency context:
<copy only dependency rows and any immediately relevant prior rows>

Rules:
- Do not edit the task list status yourself.
- Implement or prepare only the selected task.
- Do not work on later task IDs.
- Inspect the repository as needed.
- Run the verification commands required by the task when practical.
- Return a concise completion report containing:
  1. task ID,
  2. files changed,
  3. verification commands run and results,
  4. whether the task satisfies the Verification Criteria,
  5. any follow-up risks or blockers.
```

Wait for the subagent result before doing anything else.

### 4. Decide whether to update the task list

Mark the selected row `PREPARED` only if the subagent report says the task satisfies the verification criteria and includes enough evidence to support that claim.

If evidence is incomplete:
- ask the same subagent to continue with the missing verification if the Task tool returned a reusable `task_id`;
- otherwise invoke a fresh subagent only for verification;
- do not update the task list until verification is adequate.

### 5. Patch the task list

- Replace only the status cell for the selected task: `| OPEN |` -> `| PREPARED |` in that row.
- Keep `Retries` unchanged.
- Do not rewrite descriptions, dependency cells, or verification criteria.
- Re-read the task list after patching and confirm the selected row is now `PREPARED`.

### 6. Review with a subagent

Invoke a subagent such as `general` or a project-specific task-preparer subagent. The prompt must include this exact contract:

```text
You are a reviewer subagent. Review exactly one task from the Markdown task list.

Task row:
<Markdown table row>

Dependency context:
<copy only dependency rows and any immediately relevant prior rows>

Repository context:
<provide repository path, branch/commit if available, and any relevant changed files if known>

Evidence output path:
<example: evidence/reviews/task-<ID>-review.md>

Rules:

* Do not edit the task list status yourself.
* Do not repair, refactor, or improve implementation code.
* Do not work on later task IDs.
* Do not reinterpret the task beyond its Description, Testing Coverage Exceptions, and Verification Criteria.
* Treat the task’s Verification Criteria as the source of truth.
* Verify that the selected task status is `PREPARED`.
* Verify that all dependency task IDs are already `PREPARED` or `PASSED`.
* Inspect the repository as needed.
* Run the verification commands required by the task when practical.
* If a required command cannot be run, record why.
* Missing, stale, ambiguous, or unverifiable evidence is a review failure unless the task explicitly allows that exception.
* Save a review evidence file at the requested evidence output path.
* Return a concise review report.

Review procedure:

1. Parse the task row:

   * task ID,
   * component,
   * static aspect,
   * status,
   * retries,
   * description,
   * dependencies,
   * testing coverage exceptions,
   * verification criteria.

2. Check preconditions:

   * The selected task status must be `PREPARED`.
   * All dependency rows listed in `Depends On (ID)` must be `PREPARED` or `PASSED`.
   * The review must concern only the selected task.
   * The preparation report must claim the task is complete or ready for review.

3. Build a checklist from the Verification Criteria:

   * Split the Verification Criteria into concrete, testable claims.
   * Create one checklist item per claim.
   * For each item, identify the evidence required: command output, test result, coverage report, file inspection, launch evidence, or documentation check.

4. Review the implementation:

   * Inspect changed files and relevant existing files.
   * Confirm the implementation matches the selected task.
   * Confirm it does not silently implement later task IDs.
   * Confirm it does not violate dependency, architecture, runtime, or coverage constraints stated by the task.

5. Run verification:

   * Run the exact commands required by the task when practical.
   * Prefer repository-standard commands when available.
   * Record command, working directory, exit code, and result.
   * Include paths to logs, reports, coverage output, or screenshots if applicable.

6. Decide:

   * Recommend `PASSED` only if every required verification criterion is directly satisfied and required evidence is saved.
   * Recommend `REJECTED` if any criterion fails, evidence is missing, dependencies are not passed, status is not `PREPARED`, or verification cannot be trusted.
   * Do not use any other final status.

7. Save evidence:
   Create or overwrite the evidence file at:

   <Evidence output path>

   The evidence file must contain:

   * task ID,
   * review decision,
   * reviewed task row summary,
   * dependency check result,
   * checklist generated from Verification Criteria,
   * commands run with exit codes,
   * files inspected,
   * coverage evidence if relevant,
   * failures or risks,
   * recommended repair instructions if rejected.

Evidence file template:

```markdown
# Review Evidence: Task <ID> — <Static Aspect>

## Decision

Recommended status: `<PASSED or REJECTED>`

Reason: <one concise sentence>

## Task Reviewed

- ID: <ID>
- Component: <Component>
- Static Aspect: <Static Aspect>
- Input Status: <Status before review>
- Retries: <Retries>
- Depends On: <dependency IDs>

## Dependency Check

| Dependency ID | Expected Status | Observed Status | Result |
|---|---|---|---|
| <ID> | PASSED | <observed> | <PASS/FAIL> |

## Verification Checklist

| # | Criterion | Evidence Type | Result | Evidence Summary |
|---|---|---|---|---|
| 1 | <criterion> | <command/file/coverage/manual evidence> | <PASS/FAIL> | <summary> |
| 2 | <criterion> | <command/file/coverage/manual evidence> | <PASS/FAIL> | <summary> |

## Commands Run

| Command | Working Directory | Exit Code | Result |
|---|---|---:|---|
| `<command>` | `<path>` | <code> | <PASS/FAIL> |

## Files Inspected

| File | Reason | Finding |
|---|---|---|
| `<path>` | <reason> | <finding> |

## Coverage / Exception Review

Testing Coverage Exceptions from task:

> <copy exception text>

Coverage finding:

<coverage result, report path, or explanation why coverage was not applicable>

## Failure Details

Complete this section only if rejected.

### Failed Criteria

- <failed criterion and why>

### Missing Evidence

- <missing evidence, if any>

### Repair Instructions

A repair agent should:
- <specific fix>
- <specific command to rerun>
- <specific evidence to regenerate>

The repair agent should not:
- <boundaries, unrelated files, later tasks, etc.>
```

Return format:

1. task ID,
2. evidence file path,
3. recommended status: `PASSED` or `REJECTED`,
4. checklist summary,
5. commands run and results,
6. files inspected,
7. reason for the decision,
8. repair instructions if rejected.

Final response format:

```text
Task ID: <ID>
Evidence: <path>
Recommended status: <PASSED or REJECTED>

Checklist:
- PASS/FAIL - <criterion summary>
- PASS/FAIL - <criterion summary>

Commands:
- <command> -> <result>

Files inspected:
- <path> - <reason>

Decision reason:
<one paragraph>

Repair instructions:
<only if rejected>
```


### 6. Continue or stop

- If the user asked for one task, stop after successful `OPEN` -> `PREPARED` transition.
- If the user asked to process all actionable tasks, loop back to step 2.
- If the task has been marked as `REJECTED`, delegate to subagent from step 3 with the checklist as additional context.
- If several tasks are `OPEN` or `REJECTED` and do not depend on each other and do not change the same files, you can build them in parallel.
- Same thing with running reviews for `PREPARED` tasks.
