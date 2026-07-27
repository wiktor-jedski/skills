---
name: phase-orchestrator
description: MUST use this skill when asked to process a Markdown task table by delegating each OPEN task to a separate subagent, waiting for completion, reviewing PREPARED work with function-level evidence, and changing only justified task statuses.
---

# Phase Orchestrator

Prepare and review task-list work without letting passing tests substitute for code inspection. The parent coordinates; independent subagents implement and review one task at a time.

## Inputs

- Task list: `tasks.md` unless the user names another file.
- Preparation transition: `OPEN` -> `PREPARED`.
- Review recommendation: `PREPARED` -> `PASSED` or `REJECTED`.
- Valid statuses: `OPEN`, `PREPARED`, `REJECTED`, `PASSED`.

Required columns: `ID`, `Component`, `Static Aspect`, `Status`, `Retries`, `Description`, `Depends On (ID)`, `Testing Coverage Exceptions`, `Verification Criteria`.

## Hard rules

1. Delegate implementation and review. The parent must not implement task code when a writable subagent is available.
2. Use one fresh preparation subagent per task. Never let an implementation or repair subagent review its own work.
3. Run independent tasks concurrently only when their dependencies and changed files do not overlap.
4. Give each subagent only the selected row, necessary dependency rows, repository context, and verification criteria.
5. Do not change a task status merely because work or review started.
6. Change only the selected row's `Status` cell; preserve every other cell and formatting.
7. Mark `PREPARED` only after implementation evidence satisfies the task criteria.
8. Recommend `PASSED` only after acceptance review and exhaustive changed-symbol review both pass.
9. A review must use a task-specific baseline. If the task-owned diff cannot be established reliably, recommend `REJECTED` for unverifiable scope.
10. Every added or modified executable symbol must have an audit row. This includes functions, methods, behavioral types, SQL statements, routes, scripts, and configuration logic. Generated artifacts may be grouped only with a recorded justification.
11. Passing tests, coverage, build, vet, lint, or traceability checks never replace manual line-by-line inspection.
12. Every reviewer must invoke `code-review-skill` exactly once and use its relevant language guide. If that skill is unavailable, record the missing capability and recommend `REJECTED`; do not silently downgrade the review.
13. Use the severity vocabulary from `code-review-skill`. Any unresolved blocking or important finding requires `REJECTED`. Optional/nit findings may accompany `PASSED` but must remain visible in evidence.
14. Record a content hash for every reviewed implementation file. Evidence is stale when any recorded hash no longer matches; stale evidence cannot support `PASSED` until the affected symbols are reviewed again.
15. Save review evidence with `templates/review_checklist.md`. Read that template completely before starting each review. It is the single review-template source of truth; do not reproduce a second template in prompts.
16. Reuse the preparation subagent for repairs when possible. Re-review with the independent review subagent; after two repair cycles, use a fresh reviewer to counter anchoring.
17. Run `python3 scripts/validate_review_evidence.py <evidence-file>` before accepting a review decision. A validation failure blocks every task-status update.

## 1. Validate and select tasks

1. Parse task IDs as integers. Treat `-` or an empty dependency cell as no dependencies.
2. Abort on duplicate IDs or dependencies that reference missing IDs.
3. A preparation task is eligible only when its status is exactly `OPEN` and every dependency is `PASSED` or `PREPARED`.
4. Sort eligible tasks by numeric ID and select the smallest, except independent non-overlapping tasks may run concurrently.
5. If nothing is eligible, list blocked task IDs and unmet dependencies.

## 2. Capture the preparation baseline

Before delegating, capture enough state to distinguish task-owned changes from pre-existing dirty-worktree changes:

- current commit or other fixed reference;
- `git status --short`;
- hashes of already modified/untracked candidate files when practical;
- preparation report/evidence path.

The preparation subagent must record its exact changed paths and added/modified symbols. If work is already present, it must identify the best available originating patch, commit, or evidence and state baseline confidence.

## 3. Delegate preparation

Use this contract:

```text
You are a task-preparation subagent. Prepare exactly one task from the Markdown task list.

Task row:
<full selected row>

Dependency context:
<only required dependency rows and immediately relevant prior rows>

Repository and baseline context:
<repository path, fixed reference, initial status/hashes, evidence path>

Rules:
- Do not edit the task-list status.
- Implement only the selected task; do not implement later IDs.
- Preserve unrelated user changes.
- Inspect the repository and run required verification when practical.
- Record every changed path and every added/modified symbol.
- Return: task ID; files and symbols changed; baseline/reference used; commands and results; whether every verification criterion is satisfied; risks or blockers.
```

Wait for completion. If evidence is incomplete, ask the same subagent to finish verification. Mark only that row `PREPARED` when the criteria are directly supported. Otherwise leave it `OPEN` unless the user explicitly requests `REJECTED`.

## 4. Establish the review surface

Before delegating review:

1. Confirm task status is `PREPARED` and dependencies are `PREPARED` or `PASSED`.
2. Establish the task-owned diff from the preparation baseline, patch, commit, report, or before/after hashes.
3. Enumerate all changed files and executable symbols. Use language-aware discovery plus diff inspection; do not rely only on the preparation report.
4. Identify callers, callees, interfaces, tests, design/requirement sources, and persistence/API boundaries for each non-trivial symbol.
5. Compare current file hashes with prior review evidence. Add any stale affected symbols to the current review surface.

## 5. Delegate independent review

Use this contract:

```text
You are an independent reviewer subagent. Review exactly one PREPARED task. Do not repair implementation code or edit the task list.

Task row:
<full selected row>

Dependency context:
<required rows only>

Repository, baseline, and changed-surface context:
<path, fixed reference/patch, preparation evidence, changed files and known symbols>

Evidence output path:
<review path>

Mandatory process:
1. Read the phase-orchestrator review template completely.
2. Invoke code-review-skill exactly once and read its relevant language guide.
3. Independently reconstruct the task-owned diff and complete changed-symbol inventory.
4. Build acceptance checklist items from every Verification Criteria clause.
5. Inspect every changed symbol line by line, plus its callers, dependencies, tests, and design source.
6. For every non-trivial symbol examine normal behavior, edge/malformed input, every error return, state changes, cleanup, context/cancellation, concurrency, cross-process behavior, security boundaries, complexity, allocations/I/O, duplication, API necessity, language idioms, and missing adversarial tests. Record N/A with a reason.
7. Run required commands and appropriate static analysis. Record commands, working directories, exit codes, and artifacts.
8. Record all findings with severity and exact location. Passing tests are not evidence that no finding exists.
9. Record hashes for every reviewed implementation file.
10. Complete templates/review_checklist.md. Do not omit or collapse its symbol-audit sections.
11. Run the phase-orchestrator evidence validator and correct structural omissions before returning.

Decision:
- PASSED only when every acceptance criterion and every symbol audit passes, evidence is current, and no blocking/important finding remains.
- REJECTED for failed criteria, missing/stale evidence, uncertain task scope, unaudited symbols, unavailable code-review-skill, or unresolved blocking/important findings.

Return: task ID; evidence path; PASSED/REJECTED; acceptance summary; symbol-audit count; findings; commands; file hashes; decision reason; repair instructions if rejected.
```

## 6. Required function-level audit

For each symbol, the reviewer must answer with evidence:

- What contract and invariant does it implement?
- Who calls it and what assumptions cross that boundary?
- Are nil/empty/boundary/malformed values handled?
- Is each error classified, wrapped, returned, or observed correctly?
- Are files, processes, goroutines, locks, transactions, and temporary resources released on every path?
- Does cancellation work while waiting as well as while executing?
- Is coordination valid across threads and application instances?
- Can user-controlled data reach SQL, paths, commands, logs, identifiers, or trusted totals?
- Are loops, queries, allocations, conversions, and serialization bounded?
- Is functionality duplicated, aliased, unreachable, or needlessly public?
- Is the implementation idiomatic for the repository's language/toolchain?
- Which existing test proves each important branch, and which adversarial case is missing?

Trivial symbols still require a row; the audit may be concise. A file-level summary is not a substitute.

## 7. Decide, repair, and re-review

- Run `python3 <phase-orchestrator-dir>/scripts/validate_review_evidence.py <evidence-file>` and validate that the evidence agrees with the returned decision. Then change only the selected row's status from `PREPARED` to the recommended `PASSED` or `REJECTED` and re-read the row to confirm it. Do not update status from a summary alone.
- If `PASSED`, retain the complete evidence file and report the decision.
- If `REJECTED`, give the preparation/repair subagent the exact failed criteria and findings. Do not broaden repair scope.
- Re-run all affected acceptance and symbol audits after repair; do not merely verify the changed line.
- If later tasks change a reviewed file, compare hashes and re-review affected prior-task symbols before relying on the old decision.
- Before the phase ends, audit all review manifests for stale hashes and list any evidence requiring refresh.

## 8. Continue or stop

- For one requested task, stop after its requested preparation/review outcome.
- For all actionable tasks, loop to selection.
- Before ending, report changed task IDs, review decisions, stale evidence refreshed, and tasks still open or blocked.
