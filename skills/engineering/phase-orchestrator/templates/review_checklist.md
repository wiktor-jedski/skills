# Review Evidence: Task {{TASK_ID}} — {{STATIC_ASPECT}}

```yaml
task_id: {{TASK_ID}}
component: "{{COMPONENT}}"
static_aspect: "{{STATIC_ASPECT}}"
input_status: "{{STATUS_BEFORE_REVIEW}}" # expected: PREPARED
review_decision: "{{PASSED_OR_REJECTED}}"
reviewed_at_utc: "{{ISO_TIMESTAMP}}"
review_agent: "{{AGENT_NAME_OR_RUN_ID}}"
evidence_file: "evidence/reviews/task-{{TASK_ID}}-review.md"
repair_context_required: {{true_or_false}}
```

## 1. Task Source

**Description**

{{TASK_DESCRIPTION}}

**Depends On**

{{DEPENDS_ON_IDS}}

**Testing Coverage Exceptions**

{{TESTING_COVERAGE_EXCEPTIONS}}

**Verification Criteria**

{{VERIFICATION_CRITERIA}}

## 2. Pre-Review Gates

* [ ] Task status is `PREPARED`.
* [ ] All dependency task IDs listed in `Depends On` are `PASSED`.
* [ ] The implementation changes are traceable to this task.
* [ ] The review agent did not make production-code changes.
* [ ] The review is based on the current repository state, not stale logs.

Result:

```yaml
pre_review_gates_passed: {{true_or_false}}
blocking_issue: "{{NONE_OR_REASON}}"
```

## 3. Acceptance Criteria Checklist

For each sentence or clause in `Verification Criteria`, create one checklist item.

| # | Criterion       | Evidence Required              | Result        | Evidence             |
| - | --------------- | ------------------------------ | ------------- | -------------------- |
| 1 | {{CRITERION_1}} | {{COMMAND_FILE_OR_INSPECTION}} | {{PASS_FAIL}} | {{EVIDENCE_SUMMARY}} |
| 2 | {{CRITERION_2}} | {{COMMAND_FILE_OR_INSPECTION}} | {{PASS_FAIL}} | {{EVIDENCE_SUMMARY}} |
| 3 | {{CRITERION_3}} | {{COMMAND_FILE_OR_INSPECTION}} | {{PASS_FAIL}} | {{EVIDENCE_SUMMARY}} |

Rules:

* Mark `PASS` only when the criterion is directly proven.
* Mark `FAIL` when evidence is missing, stale, ambiguous, or contradicted.
* Do not treat successful build/test output as sufficient unless it proves the specific criterion.
* Coverage exceptions are allowed only when they match the task’s `Testing Coverage Exceptions` text.

## 4. Commands Run

Record every command used as evidence.

```bash
{{COMMAND_1}}
{{COMMAND_2}}
{{COMMAND_3}}
```

For each command:

| Command       | Exit Code     | Result        | Log / Artifact          |
| ------------- | ------------- | ------------- | ----------------------- |
| `{{COMMAND}}` | {{EXIT_CODE}} | {{PASS_FAIL}} | {{LOG_PATH_OR_SUMMARY}} |

## 5. Files Inspected

| File            | Purpose           | Finding     |
| --------------- | ----------------- | ----------- |
| `{{FILE_PATH}}` | {{WHY_INSPECTED}} | {{SUMMARY}} |

## 6. Coverage Review

* [ ] Required coverage command was run, unless the task explicitly allows an exception.
* [ ] Coverage report path is recorded.
* [ ] Required line coverage threshold was met.
* [ ] Untested branches relevant to the task were checked.
* [ ] Any coverage exception is copied from the task row and justified.

Coverage evidence:

```yaml
coverage_required: {{true_or_false}}
coverage_exception_allowed: {{true_or_false}}
coverage_report_path: "{{PATH_OR_NONE}}"
observed_line_coverage: "{{VALUE_OR_NA}}"
coverage_passed: {{true_or_false}}
```

## 7. Negative / Regression Checks

* [ ] Existing tests still pass.
* [ ] No unrelated runtime dependencies were introduced.
* [ ] No unrelated architectural boundary was changed.
* [ ] No source-of-truth documentation was contradicted.
* [ ] No generated, cache, build, or temporary files were committed as evidence unless intentionally required.

Findings:

{{NEGATIVE_CHECK_FINDINGS}}

## 8. Review Decision

A task may be marked `PASSED` only when:

* every required acceptance criterion passes;
* every required command passes;
* required evidence is saved;
* exceptions are explicitly allowed by the task row;
* no blocking regression is found.

Decision:

```yaml
decision: "{{PASSED_OR_REJECTED}}"
reason: "{{ONE_SENTENCE_REASON}}"
failed_criteria:
  - "{{FAILED_CRITERION_OR_EMPTY}}"
recommended_next_action: "{{NONE_OR_REPAIR_AGENT_INSTRUCTIONS}}"
```

## 9. Repair Context

Complete this section only when `decision: REJECTED`.

### Failure Summary

{{WHAT_FAILED}}

### Minimal Repair Goal

{{WHAT_THE_REPAIR_AGENT_SHOULD_FIX}}

### Evidence To Reuse

{{LOGS_REPORTS_FILES_TO_GIVE_REPAIR_AGENT}}

### Do Not Change

{{BOUNDARIES_OR_WORKING_BEHAVIOR_THAT_SHOULD_NOT_BE_MODIFIED}}
