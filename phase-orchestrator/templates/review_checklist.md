# Review Evidence: Task {{TASK_ID}}

```yaml
task_id: {{TASK_ID}}
review_agent: "{{AGENT_NAME_OR_RUN_ID}}"
```

## 1. Task Source

**Description:** {{TASK_DESCRIPTION}}

**Dependencies:** {{DEPENDENCY_IDS}}

**Verification criteria:** {{VERIFICATION_CRITERIA}}

## 2. Pre-Review Gates

- [ ] The task status is `PREPARED`.
- [ ] All dependencies are `PASSED`.
- [ ] The review boundary is clear.
- [ ] `code-review-skill` was invoked exactly once.
- [ ] The reviewer read the relevant language guide.
- [ ] The reviewer did not change implementation code or the task list.

```yaml
pre_review_gates_passed: {{true_or_false}}
blocking_issue: "{{NONE_OR_REASON}}"
```

## 3. Review Surface

Review boundary: {{BOUNDARY}}

Commands used to reconstruct the diff:

```bash
{{DIFF_COMMANDS}}
```

| Changed file | Purpose     | Symbols or units |
| ------------ | ----------- | ---------------- |
| `{{PATH}}`   | {{PURPOSE}} | {{SYMBOLS}}      |

## 4. Acceptance Criteria

Create one row for each testable clause.

|   # | Criterion     | Evidence     | Result           |
| --: | ------------- | ------------ | ---------------- |
|   1 | {{CRITERION}} | {{EVIDENCE}} | {{PASS_OR_FAIL}} |

## 5. Changed-Symbol Inventory

List every added or modified executable unit. This includes functions, methods,
behavioral types, SQL statements, routes, scripts, and configuration logic.

<!-- markdownlint-disable MD013 -->

|   # | Symbol or unit | Kind     | File and line       | Callers or consumers | Tests     |
| --: | -------------- | -------- | ------------------- | -------------------- | --------- |
|   1 | `{{SYMBOL}}`   | {{KIND}} | `{{PATH_AND_LINE}}` | {{CALLERS}}          | {{TESTS}} |

<!-- markdownlint-enable MD013 -->

```yaml
inventory_source_count: {{COUNT}}
inventory_complete: {{true_or_false}}
```

## 6. Function-Level Audit

Use `N/A` with a reason when an item does not apply.

<!-- markdownlint-disable MD013 -->

| Symbol or unit | Contract and paths     | State and resources     | Security and bounds     | Quality and idioms     | Tests and gaps     | Result           |
| -------------- | ---------------------- | ----------------------- | ----------------------- | ---------------------- | ------------------ | ---------------- |
| `{{SYMBOL}}`   | {{CONTRACT_AND_PATHS}} | {{STATE_AND_RESOURCES}} | {{SECURITY_AND_BOUNDS}} | {{QUALITY_AND_IDIOMS}} | {{TESTS_AND_GAPS}} | {{PASS_OR_FAIL}} |

<!-- markdownlint-enable MD013 -->

```yaml
audited_symbol_count: {{COUNT}}
```

## 7. Findings

Record all findings. Use the severity terms from `code-review-skill`.

<!-- markdownlint-disable MD013 -->

| Severity             | File and line       | Symbol       | Problem     | Required repair or disposition |
| -------------------- | ------------------- | ------------ | ----------- | ------------------------------ |
| {{SEVERITY_OR_NONE}} | `{{PATH_AND_LINE}}` | `{{SYMBOL}}` | {{PROBLEM}} | {{ACTION}}                     |

<!-- markdownlint-enable MD013 -->

```yaml
blocking_findings: {{COUNT}}
important_findings: {{COUNT}}
optional_findings: {{COUNT}}
```

## 8. Commands Run

| Command       | Working directory | Exit code | Result           |
| ------------- | ----------------- | --------: | ---------------- |
| `{{COMMAND}}` | `{{PATH}}`        |  {{CODE}} | {{PASS_OR_FAIL}} |

Record why a required command did not run.

## 9. Coverage and Exceptions

```yaml
coverage_required: {{true_or_false}}
coverage_exception_allowed: {{true_or_false}}
coverage_report_path: "{{PATH_OR_NONE}}"
observed_line_coverage: "{{VALUE_OR_NA}}"
coverage_passed: {{true_or_false}}
```

Finding: {{COVERAGE_FINDING}}

## 10. Negative and Regression Checks

- [ ] Focused existing tests pass.
- [ ] The change adds no unrelated dependency or boundary.
- [ ] The change does not contradict a source document.
- [ ] The change adds no unintended generated or temporary file.
- [ ] Each new public API is necessary and used.
- [ ] No duplicate helper or obsolete alias remains.
- [ ] Error, cleanup, timeout, concurrency, and malformed-input paths were
      checked.

Findings: {{NEGATIVE_CHECK_FINDINGS}}

## 11. Decision

Run:

```bash
python3 <phase-orchestrator-dir>/scripts/validate_review_evidence.py <this-file>
```

```yaml
decision: "{{PASSED_OR_REJECTED}}"
reason: "{{ONE_SENTENCE_REASON}}"
failed_criteria:
  - "{{FAILED_CRITERION_OR_NONE}}"
failed_or_unaudited_symbols:
  - "{{SYMBOL_OR_NONE}}"
repair_instructions: "{{REPAIR_OR_NONE}}"
```
