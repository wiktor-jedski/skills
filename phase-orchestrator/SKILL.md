---
name: phase-orchestrator
description: Orchestrate implementation, review, and integration of phase tasks.
disable-model-invocation: true
---

# Phase Orchestrator

Process a phase task graph with dedicated OMP subagents in isolated Git
worktrees.

## Inputs

Use the task list specified by the applicable `AGENTS.md`. Use another task list
only when the user specifies it. The task-details directory is `tasks/` beside
the task list.

The table must contain:

`ID | Architecture Component | Status | Depends On (ID)`

`Architecture Component` must contain at least one architecture component
identifier. Valid statuses are `OPEN`, `PREPARED`, and `PASSED`.

Each task must have `tasks/{ID}.md` with `Description` and
`Acceptance Criteria` sections. The task file is the source of implementation
scope, design references, commands, and observable pass conditions.

## Hard truths

- OMP subagent tools are the orchestration mechanism. Spawn agents with `task`,
  inspect them with `hub` `list` and `jobs`, answer active-delegation questions
  with `hub` `send`, and wait with `hub` `wait`.
- Use a fresh `developer` OMP agent for every preparation, repair, integration,
  and publication delegation. Use a fresh `reviewer` OMP agent for every task
  review and integration review cycle. Agent definitions supply their roles and
  tools.
- Fill the available concurrency with eligible tasks at the start and after
  every wake-up. Parallel work is safe only when every listed dependency of
  every selected task is already `PASSED`; `PREPARED` and in-flight dependencies
  are unmet.
- A task follows this complete gate sequence: prepare -> task review ->
  integrate -> integration review -> publish -> mark `PASSED`. No gate is
  optional.
- Every bounded stage delegation gets a newly spawned agent with fresh context.
  Never reuse an agent for another stage, repair attempt, or review cycle, even
  for the same task and role. Use `hub` `send` only to answer a question or
  request missing bounded evidence while that original delegation remains
  active.
- The orchestrator owns scheduling and the task list. Subagents own
  implementation, review, and integration work.
- Waiting is the steady state while work is in flight. Call
  `hub` with `op: "wait"` and `timeoutMs: 3600000`. A timeout starts another
  longest-timeout wait; an agent event starts the wake cycle below.

Repository scripts are task artifacts, not an agent-launch mechanism. Run
orchestration exclusively through the OMP subagent tools above.

## Role context

Resolve these paths before scheduling:

- Preparation template: `<skill-directory>/PREPARATION.md`
- Review template: `<skill-directory>/REVIEW.md`
- Integration template: `<skill-directory>/INTEGRATION.md`
- State machine: `<skill-directory>/STATE_MACHINE.md`

Read `STATE_MACHINE.md` completely before bootstrap and immediately after every
`hub` wait return. Treat it as the single source of truth for cycle inputs,
scheduling decisions, and task transitions.

Immediately before every OMP subagent delegation:

1. Read the complete workflow template for the requested stage.
2. Give the agent the task ID, absolute workflow-template path, stage, and the
   bounded result or repair evidence it needs.

Use this base delegation:

```text
Read <absolute-template-path> completely and follow it as your workflow template.
Task ID: <ID>
Task file: <absolute-task-details-directory>/<ID>.md
Stage: <stage>
Assigned worktree: <absolute-worktree-path>
Bounded stage input: <durable Git identities and accepted or rejected evidence>
```

The subagent gets repository context from `AGENTS.md`, the task list, the task
file, and Git. The orchestrator does not perform the delegated role.

## Run ledger

Maintain one row per active task:

```text
Task | Stage | Active delegation agent | Outstanding work | Accepted evidence | Agent history
```

The ledger is the authoritative record of current runtime state.
`STATE_MACHINE.md` defines the transition rules. Record every spawned agent in
the history with its bounded stage, and keep only the current delegation's agent
in the active field. Before spawning, consult the ledger and `hub` agent/job
snapshots for capacity and duplicate outstanding work; never select a historical
agent for new work.

## Rules

- Work only in a Git repository.
- Start only when the phase worktree is clean.
- The orchestrator owns the task list. Other agents do not edit it.
- Change only the selected status cell. Preserve all other cells and table
  format.
- Integrate and publish one task at a time; preparation and task review may run
  concurrently across eligible tasks.
- Keep each merged task branch.
- Remove each task worktree and temporary integration branch after the task
  passes.
- Send one complete delegation for a bounded stage. While that agent is active,
  wait for its result and respond only to a question or blocker that requires
  orchestration input.
- Stop an agent only when the user cancels the work.

## Process

### 1. Bootstrap

Parse task IDs as integers. Treat `-` and an empty dependency cell as no
dependencies.

Stop if an ID is not unique, an architecture component is missing, a dependency
is missing, a status is invalid, a task file is missing or malformed, the
repository is not clean, or required role/template files cannot be read.

Create the run ledger for every task-list row. An `OPEN` task is eligible only
when all its dependencies are `PASSED`. A `PREPARED` task resumes at task review
unless the ledger or durable Git evidence proves a later stage.

Bootstrap is complete when every task has a valid state and every immediately
eligible task is identified.

### 2. Schedule a frontier

Follow the scheduler in `STATE_MACHINE.md`. Sort eligible tasks by integer ID.
Starting with the smallest IDs, dispatch as many preparation delegations in one
scheduling pass as the available agent capacity supports. Issue the entire
frontier back-to-back before the first wait. Create each worktree detached at
the current phase-branch commit in `../worktrees/<project-name>/<task-id>/`; the
developer creates the task branch there.

Two tasks may share already-passed ancestors. They are never in the same
frontier when either task depends transitively on the other.

Do not reserve work for a future dependency level while runnable frontier work
has capacity. Scheduling is complete when every eligible task is either in
flight or excluded by the current capacity limit.

### 3. Wake cycle

Immediately after every wait returns, reread `STATE_MACHINE.md` completely,
collect its cycle inputs, and execute every box in its orchestrator cycle in
order.

The wake cycle is complete only when every received event has a transition, all
safe capacity is filled, and the orchestrator is waiting or the phase is
terminal.

### 4. Prepare

The fresh preparation developer implements and commits the task on its task
branch.
Accept preparation only when the developer satisfies every completion criterion
in `PREPARATION.md` with direct evidence and the task worktree is clean.

After acceptance, change only that task's status from `OPEN` to `PREPARED`, then
commit and push the task-list change on the phase branch.

### 5. Task review

Spawn a fresh reviewer to review the prepared task using `REVIEW.md`.

Accept `PASSED` only with the required checklist, complete inventory,
acceptance-criteria evidence, and successful evidence validation. On `REJECTED`,
keep the task `PREPARED`; spawn a fresh developer with the complete findings.
After accepting the repair result, spawn another fresh reviewer for a complete
task review.

Task review is complete only when the current review cycle returns an
evidence-backed `PASSED`.

### 6. Integrate and review

Integrate one approved task at a time. Spawn a fresh developer using
`INTEGRATION.md`. The developer creates a temporary integration branch from the
remote phase branch, merges the approved task branch, resolves any conflicts,
and runs the integration checks without publishing.

Only an integrated result with passing checks proceeds to review. If integration
or repair checks fail, spawn a fresh developer for an integration-repair
delegation with the branch, commit, failed commands, and complete output. Each
failed repair attempt produces another fresh repair agent.

After checks pass, spawn a fresh reviewer for the complete integrated result. On
rejection, spawn a fresh developer to repair the temporary integration branch,
then spawn another fresh reviewer for a complete integration review.

Integration is complete only when the reviewer returns an evidence-backed
`PASSED` for the current temporary integration branch.

### 7. Publish and complete

After integration review passes, spawn a fresh developer for publication. The
developer pushes the exact reviewed temporary integration branch to the remote
phase branch with a normal fast-forward push.

Then the orchestrator:

1. Runs `git pull --ff-only` in the phase worktree.
2. Changes only the task status from `PREPARED` to `PASSED`.
3. Commits and pushes the task-list change.
4. Removes the task worktree and temporary integration branch.
5. Keeps the merged task branch.
6. Marks the task terminal in the ledger.

Completion is reached only when the merge is published, the `PASSED` status is
published, cleanup succeeds, and no gate lacks accepted evidence.

For one requested task, stop after its completion. For all actionable tasks, run
the wake cycle and schedule the newly eligible frontier.

If no work is in flight and no task is eligible, report every blocked task and
its unmet dependencies.

Report only:

- Task IDs that changed.
- Open or blocked tasks, if any.
