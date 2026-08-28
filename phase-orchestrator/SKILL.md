---
name: phase-orchestrator
description: Orchestrate implementation, review, and integration of phase tasks.
disable-model-invocation: true
---

# Phase Orchestrator

Process a phase task graph with dedicated Codex subagents in isolated Git
worktrees.

## Inputs

Use the task list specified by the applicable `AGENTS.md`. Use another task list
only when the user specifies it.

The table must contain:

`ID | Status | Description | Depends On (ID) | Verification Criteria`

Valid statuses are `OPEN`, `PREPARED`, and `PASSED`.

## Hard truths

- Codex collaboration tools are the orchestration mechanism. Create agents with
  `spawn_agent`, continue them with `followup_task`, inspect them with
  `list_agents`, and wait with `wait_agent`.
- Use the `developer` agent type for preparation, repair, integration, and
  publication. Use the `reviewer` agent type for task and integration reviews.
  These types load the role profiles from `~/.codex/agents/developer.toml` and
  `~/.codex/agents/reviewer.toml`.
- Fill the available concurrency with eligible tasks at the start and after
  every wake-up. Parallel work is safe only when every listed dependency of
  every selected task is already `PASSED`; `PREPARED` and in-flight dependencies
  are unmet.
- A task follows this complete gate sequence: prepare -> task review ->
  integrate -> integration review -> publish -> mark `PASSED`. No gate is
  optional.
- Keep one developer and one reviewer assigned to a task for its entire
  lifetime. Continue an assigned agent instead of creating another one. Create a
  replacement only when the assigned agent is unavailable, and record the
  replacement in the run ledger.
- The orchestrator owns scheduling and the task list. Subagents own
  implementation, review, and integration work.
- Waiting is the steady state while work is in flight. Call
  `wait_agent(timeout_ms=3600000)`, the longest supported wait. A timeout starts
  another longest-timeout wait; an agent event starts the wake cycle below.

Repository scripts are task artifacts, not an agent-launch mechanism. Run
orchestration exclusively through the Codex collaboration tools above.

## Role context

Resolve these paths before scheduling:

- Developer profile: `~/.codex/agents/developer.toml`
- Reviewer profile: `~/.codex/agents/reviewer.toml`
- Preparation template: `<skill-directory>/PREPARATION.md`
- Review template: `<skill-directory>/REVIEW.md`
- Integration template: `<skill-directory>/INTEGRATION.md`
- State machine: `<skill-directory>/STATE_MACHINE.md`

Read `STATE_MACHINE.md` completely before bootstrap and immediately after every
`wait_agent` return. Treat it as the single source of truth for cycle inputs,
scheduling decisions, and task transitions.

Immediately before every spawn or follow-up delegation:

1. Read the complete profile for the selected agent type.
2. Read the complete workflow template for the requested stage.
3. Give the agent the task ID, absolute workflow-template path, stage, and the
   bounded result or repair evidence it needs.

Use this base delegation:

```text
Read <absolute-template-path> completely and follow it as your workflow template.
Task ID: <ID>
Stage: <stage>
```

The subagent gets repository context from `AGENTS.md`, the task list, and Git.
The orchestrator does not perform the delegated role.

## Run ledger

Maintain one row per active task:

```text
Task | Developer | Reviewer | Stage | Outstanding work | Accepted evidence
```

The ledger is the authoritative record of current assignments and accepted
runtime state; `STATE_MACHINE.md` defines the transition rules. Before spawning,
consult both the ledger and `list_agents`. An assigned idle agent receives
`followup_task`; an unavailable assigned agent is replaced once and the ledger
is updated.

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

Stop if an ID is not unique, a dependency is missing, a status is invalid, the
repository is not clean, or required role/template files cannot be read.

Create the run ledger. An `OPEN` task is eligible only when all its dependencies
are `PASSED`. A `PREPARED` task resumes at task review unless the ledger or
durable Git evidence proves a later stage.

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

The assigned developer implements and commits the task on its task branch.
Accept preparation only when the developer satisfies every completion criterion
in `PREPARATION.md` with direct evidence and the task worktree is clean.

After acceptance, change only that task's status from `OPEN` to `PREPARED`, then
commit and push the task-list change on the phase branch.

### 5. Task review

The assigned reviewer reviews the prepared task using `REVIEW.md`.

Accept `PASSED` only with the required checklist, complete inventory,
verification evidence, and successful evidence validation. On `REJECTED`, keep
the task `PREPARED`; send the complete findings to the same developer, then send
the repair result back to the same reviewer.

Task review is complete only when that reviewer returns an evidence-backed
`PASSED`.

### 6. Integrate and review

Integrate one approved task at a time. Delegate integration to the same
developer using `INTEGRATION.md`. The developer creates a temporary integration
branch from the remote phase branch, merges the approved task branch, resolves
any conflicts, and runs the integration checks without publishing.

Delegate review of the complete integrated result to the same reviewer. On
rejection, the same developer repairs the temporary integration branch and the
same reviewer repeats the full integration review.

Integration is complete only when the reviewer returns an evidence-backed
`PASSED` for the current temporary integration branch.

### 7. Publish and complete

After integration review passes, delegate publication to the same developer. The
developer pushes the reviewed temporary integration branch to the remote phase
branch with a normal fast-forward push.

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
