# Review Evidence: Task {{TASK_ID}} — {{STATIC_ASPECT}}

```yaml
task_id: {{TASK_ID}}
component: "{{COMPONENT}}"
static_aspect: "{{STATIC_ASPECT}}"
input_status: "{{STATUS_BEFORE_REVIEW}}"
review_decision: "{{PASSED_OR_REJECTED}}"
reviewed_at_utc: "{{ISO_TIMESTAMP}}"
review_agent: "{{AGENT_NAME_OR_RUN_ID}}"
evidence_file: "{{EVIDENCE_PATH}}"
baseline_ref: "{{COMMIT_PATCH_OR_MANIFEST}}"
baseline_confidence: "{{HIGH_MEDIUM_LOW}}"
code_review_skill_invoked: {{true_or_false}}
relevant_language_guide: "{{GUIDE_OR_NONE}}"
repair_context_required: {{true_or_false}}
```

## 1. Task Source

**Description:** {{TASK_DESCRIPTION}}

**Depends On:** {{DEPENDS_ON_IDS}}

**Testing Coverage Exceptions:** {{TESTING_COVERAGE_EXCEPTIONS}}

**Verification Criteria:** {{VERIFICATION_CRITERIA}}

## 2. Pre-Review Gates

- [ ] Input status is `PREPARED`.
- [ ] Every dependency is `PREPARED` or `PASSED`.
- [ ] The preparation report claims completion.
- [ ] A task-specific baseline/diff is available and trustworthy.
- [ ] `code-review-skill` was invoked exactly once and its relevant guide read.
- [ ] The reviewer is independent from implementation/repair.
- [ ] Review uses current repository state rather than stale logs.
- [ ] Reviewer made no production-code changes.

```yaml
pre_review_gates_passed: {{true_or_false}}
blocking_issue: "{{NONE_OR_REASON}}"
```

## 3. Review Baseline and Change Surface

Baseline/reference method: {{HOW_BASELINE_WAS_ESTABLISHED}}

Commands used to reconstruct the diff:

```bash
{{DIFF_AND_DISCOVERY_COMMANDS}}
```

Pre-existing dirty-worktree changes and exclusions:

{{PRE_EXISTING_CHANGES_AND_SCOPE_BOUNDARIES}}

| Changed file | Change source | Task-owned confidence | Symbols/units discovered |
|---|---|---|---|
| `{{PATH}}` | {{DIFF_COMMIT_REPORT}} | {{HIGH_MEDIUM_LOW}} | {{SYMBOLS}} |

If any task-owned change cannot be distinguished reliably, stop and recommend `REJECTED`.

## 4. Acceptance Criteria Checklist

Create one row for every sentence or independently testable clause in `Verification Criteria`.

| # | Criterion | Evidence required | Result | Evidence |
|---:|---|---|---|---|
| 1 | {{CRITERION}} | {{COMMAND_FILE_COVERAGE_INSPECTION}} | {{PASS_FAIL}} | {{SUMMARY}} |

Passing a broad command is insufficient unless it directly proves the criterion.

## 5. Changed-Symbol Inventory

Inventory every added or modified executable unit. Include functions, methods, behavioral types, SQL statements, routes, scripts, and configuration logic. Group generated artifacts only with a justification.

| # | Symbol/unit | Kind | File:line | Added/modified | Callers or consumers | Tests |
|---:|---|---|---|---|---|---|
| 1 | `{{SYMBOL}}` | {{FUNCTION_SQL_ROUTE_ETC}} | `{{PATH_LINE}}` | {{CHANGE}} | {{CALLERS}} | {{TESTS}} |

```yaml
inventory_source_count: {{COUNT_FROM_DIFF}}
audited_symbol_count: {{COUNT_AUDITED}}
inventory_complete: {{true_or_false}}
generated_groupings:
  - "{{GROUP_AND_JUSTIFICATION_OR_NONE}}"
```

`inventory_source_count` and `audited_symbol_count` must match. Otherwise recommend `REJECTED`.

## 6. Function-Level Audit

Complete one row per inventory entry. Use `N/A — <reason>` rather than leaving a cell blank.

| Symbol/unit | Contract and invariants | Normal/edge/error paths | State/resources/cancellation/concurrency | Security boundaries | Performance/allocations/I/O | Simplicity/API/idioms | Tests and adversarial gaps | Result |
|---|---|---|---|---|---|---|---|---|
| `{{SYMBOL}}` | {{CONTRACT}} | {{PATH_AUDIT}} | {{LIFECYCLE_AUDIT}} | {{SECURITY_AUDIT}} | {{PERFORMANCE_AUDIT}} | {{QUALITY_AUDIT}} | {{TEST_AUDIT}} | {{PASS_FAIL}} |

Mandatory questions for every non-trivial unit:

- Are boundary and malformed inputs handled?
- Is every return/error path intentional and observable?
- Are resources released on success, failure, and cancellation?
- Does cancellation apply while waiting and executing?
- Is concurrency correct across threads and process instances?
- Is user-controlled data prevented from crossing trusted boundaries unsafely?
- Are loops, queries, output, memory, and subprocess work bounded?
- Is the symbol necessary, non-duplicative, minimally public, and idiomatic?
- Do tests prove adversarial behavior rather than only the happy path?

## 7. Findings

Record findings even when they do not block acceptance.

| Severity | File:line | Symbol | Problem | Evidence/trigger | Required repair or disposition |
|---|---|---|---|---|---|
| {{BLOCKING_IMPORTANT_NIT_OR_NONE}} | `{{PATH_LINE}}` | `{{SYMBOL}}` | {{PROBLEM}} | {{EVIDENCE}} | {{REPAIR}} |

```yaml
blocking_findings: {{COUNT}}
important_findings: {{COUNT}}
optional_findings: {{COUNT}}
```

Any unresolved blocking or important finding requires `REJECTED`.

## 8. Commands Run

| Command | Working directory | Exit code | Result | Log/artifact |
|---|---|---:|---|---|
| `{{COMMAND}}` | `{{PATH}}` | {{CODE}} | {{PASS_FAIL}} | {{LOG_OR_SUMMARY}} |

Include required tests plus appropriate formatting, vet/static analysis, race/security, coverage, and repository validators. Record why any required command was not run.

## 9. Files Inspected and Staleness Fingerprints

Hash the current contents of every reviewed implementation file after review.

| File | Purpose | Finding | Hash algorithm | Content hash |
|---|---|---|---|---|
| `{{PATH}}` | {{PURPOSE}} | {{FINDING}} | {{SHA256_OR_GIT_BLOB}} | `{{HASH}}` |

```yaml
all_reviewed_files_hashed: {{true_or_false}}
prior_evidence_checked_for_staleness: {{true_or_false}}
stale_prior_evidence:
  - "{{TASK_PATH_OR_NONE}}"
```

Changed hashes invalidate prior evidence for affected symbols.

## 10. Coverage and Exceptions

- [ ] Required coverage command ran, unless explicitly excepted.
- [ ] Report path and observed threshold are recorded.
- [ ] Untested branches relevant to changed symbols were inspected.
- [ ] Exceptions exactly match the task row and are justified.

```yaml
coverage_required: {{true_or_false}}
coverage_exception_allowed: {{true_or_false}}
coverage_report_path: "{{PATH_OR_NONE}}"
observed_line_coverage: "{{VALUE_OR_NA}}"
coverage_passed: {{true_or_false}}
```

Coverage finding: {{COVERAGE_FINDING}}

## 11. Negative and Regression Checks

- [ ] Existing focused tests pass.
- [ ] No unrelated dependency or architectural boundary was introduced.
- [ ] No source-of-truth documentation was contradicted.
- [ ] No generated/cache/build/temporary artifact was unintentionally added.
- [ ] Public API additions are necessary and used.
- [ ] Duplicate helpers and obsolete aliases were searched for.
- [ ] Error, cleanup, timeout, concurrency, and malformed-input paths were challenged.

Findings: {{NEGATIVE_CHECK_FINDINGS}}

## 12. Decision

A task may be `PASSED` only when all acceptance criteria and symbol audits pass, evidence is current, every reviewed file is hashed, and no blocking/important finding remains.

Before accepting the decision, run:

```bash
python3 <phase-orchestrator-dir>/scripts/validate_review_evidence.py <this-evidence-file>
```

```yaml
decision: "{{PASSED_OR_REJECTED}}"
reason: "{{ONE_SENTENCE_REASON}}"
failed_criteria:
  - "{{FAILED_CRITERION_OR_EMPTY}}"
failed_or_unaudited_symbols:
  - "{{SYMBOL_OR_EMPTY}}"
recommended_next_action: "{{NONE_OR_REPAIR_INSTRUCTIONS}}"
```

## 13. Repair Context

Complete only for `REJECTED`.

### Failure Summary

{{WHAT_FAILED}}

### Minimal Repair Goal

{{WHAT_TO_FIX}}

### Evidence to Reuse

{{LOGS_REPORTS_FILES}}

### Required Re-Review Surface

{{AFFECTED_SYMBOLS_CALLERS_TESTS}}

### Do Not Change

{{BOUNDARIES_OR_WORKING_BEHAVIOR}}
