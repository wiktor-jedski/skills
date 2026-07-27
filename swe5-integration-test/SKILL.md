---
name: swe5-integration-testing
description: Generate, maintain, and implement SWE.5 Software Integration and Integration Testing artifacts. Use when identifying architecture components ready for integration verification, generating Integration Verification Obligations from software-architecture.md, creating SWE.5 tasks in tasks.md, implementing integration tests, verifying architectural behavior across collaborating software units, maintaining traceability between ARCH-* components, SW-REQ-* requirements, obligations, and tests, or evaluating coverage using CHECKLIST.md before marking SWE.5 work complete.
---

# SWE.5 Integration Test

## Purpose

This skill implements Automotive SPICE SWE.5 Software Integration and Integration Testing activities.

The purpose of SWE.5 is to verify that software units collaborate correctly according to the software architecture.

This skill shall:

1. Identify architecture components ready for SWE.5 verification.
2. Generate Integration Verification Obligation documents.
3. Create implementation tasks for missing SWE.5 coverage.
4. Implement integration tests.
5. Maintain traceability between architecture, requirements, obligations, and tests.

---

## Definitions

### SWE.5

SWE.5 verifies collaboration between software units implementing an architecture component.

Examples:

* SceneRouter + SaveManager
* GameState + SaveContracts
* SaveManager + SaveContracts

SWE.5 tests verify architecture behavior.


---

### Obligation

An Integration Verification Obligation describes architectural behavior that must be verified.

An obligation is not a test case.

One obligation may require multiple integration tests.

---

## Source Documents

Read:

* docs/implementation/tasks.md
* docs/design/software-architecture.md
* docs/design/code-design.md

If available, also read:

* docs/testing/integration/*.md

---

## Workflow

### Step 1 - Generate SWE.5 Obligations

Execute:

```bash
python .agents/skills/swe5-integration-test/scripts/generate_swe5_obligations.py
```

The script produces JSON describing architecture components requiring SWE.5 verification.

Example:

```json
{
  "architecture_components": [
    {
      "arch_id": "ARCH-002",
      "status": "ready_for_swe5"
    }
  ]
}
```

Only process architecture components whose status is:

* ready_for_swe5
* missing_swe5

Ignore architecture components already fully covered.

---

### Step 2 - Create Obligation Documents

For each architecture component requiring SWE.5 coverage:

Create:

```text
docs/testing/integration/<ARCH-ID>-obligations.md
```

Use the Integration Verification Obligation template.

`<skill-directory>/templates/obligation.md`

Derive obligations from:

1. Architecture description.
2. Dynamic behavior.
3. Interface definitions.
4. Dependency relationships.
5. Requirement traceability.

Create obligations for:

* nominal behavior
* robustness behavior
* failure handling
* recovery behavior
* restore behavior

when applicable.

---

### Step 3 - Create SWE.5 Tasks

For each architecture component without completed SWE.5 coverage:

Create a task in:

```text
docs/implementation/tasks.md
```

Task pattern:

| Component                      | Static Aspect |
| ------------------------------ | ------------- |
| SWE.5 Integration Verification | ARCH-XXX      |

Verification criteria:

```text
All Integration Verification Obligations for ARCH-XXX are implemented and passing.
```

Do not create one task per obligation.

Create one SWE.5 task per architecture component.

---

### Step 4 - Implement Integration Tests

Implement integration tests satisfying all obligations.

Preferred location:

```text
tests/Integration/
```

or existing integration-test location used by the repository.

---

### Step 5 - Execute Integration Tests

Run the implemented tests from the previous step.

Verify that all tests pass.

---

### Step 6 - Execute Checklist

1. Read:

   * CHECKLIST.md
   * obligation document
   * implemented integration tests

Evaluate every mandatory checklist item.

---

### Step 7 - Produce Verification Report

Example:

```text
ARCH-002

IT-ARCH-002-001
PASS

IT-ARCH-002-002
PASS

IT-ARCH-002-003
FAIL

Reason:
Recovery path not verified.
```

If any mandatory checklist item fails:

* do not mark the obligation complete
* do not mark the SWE.5 task PASSED
* create follow-up work

---

### Step 8 - Update Task Status

Only mark the task PASSED when all obligations pass the checklist.

---

## Integration Test Design Rules

### Rule 1

The primary architecture component is the System Under Test.

Example:

```text
ARCH-002
```

System Under Test:

```text
UNIT-002 SceneRouter
```

---

### Rule 2

Use real collaborating units whenever practical.

Avoid excessive mocking.

Prefer:

```text
Real:
    UNIT-002
    UNIT-005
    UNIT-020

Stub:
    UNIT-006
```

over:

```text
Mock everything
```

---

### Rule 3

Verify architecture behavior.

Do not repeat unit tests.

Bad:

```text
Invalid StringId returns ERR_INVALID_ID.
```

Good:

```text
Planning transition creates checkpoint
and opens target scene only after
successful persistence.
```

---

### Rule 4

Verify interaction sequences.

Examples:

* checkpoint written before route opens
* restore performed before scene initialization
* consequence application before mission-end checkpoint creation

---

### Rule 5

Verify architectural state transitions.

Examples:

* unlocked → locked
* planning → mission
* mission_end → aftermath
* restore → active state

---

### Rule 6

Verify error handling and recovery behavior.

Examples:

* failed save activates lock
* retry uses frozen payload
* restore rejects unsupported schema

---

## Traceability

Each integration test shall contain:

```csharp
/// Verifies IT-ARCH-002-001
/// Verifies ARCH-002
/// Traces SW-REQ-012
/// Traces SW-REQ-013
```

Every obligation must be referenced by at least one test.

Every test must reference at least one obligation.

---

## Completion Criteria

SWE.5 coverage for an architecture component is complete when:

1. Obligation document exists.
2. All obligations are implemented.
3. All integration tests pass.
4. Traceability comments exist.
5. Architecture behavior is verified.
6. No obligation remains uncovered.

When all criteria are satisfied:

* update task status accordingly
* record evidence required by the repository workflow

---

## Forbidden Behaviors

Do not:

* create unit tests and label them integration tests
* mock every dependency
* duplicate SWE.4 verification
* create obligations without architecture traceability
* close SWE.5 tasks without implemented tests
* ignore failure and recovery paths

The goal is verification of architecture behavior, not verification of isolated functions.

---

## Common Failure Modes

Avoid the following anti-patterns.

### Anti-Pattern 1

Mocking every dependency.

Bad:

```text
SceneRouter
  -> mocked SaveManager
  -> mocked SaveContractFactory
  -> mocked UIFeedbackService
```

Result:

Unit test disguised as integration test.

---

### Anti-Pattern 2

Rewriting SWE.4 tests.

Bad:

```text
ValidateCampaignState rejects invalid IDs.
```

This is a unit test.

---

### Anti-Pattern 3

Testing implementation details.

Bad:

```text
Verify internal private method execution.
```

Verify architecture behavior instead.

---

### Anti-Pattern 4

Single-obligation giant tests.

Bad:

```text
One test validates every obligation.
```

Create focused tests.

---

### Anti-Pattern 5

Closing obligations without evidence.

Every obligation must be traceable to:

* architecture component
* requirement
* test implementation
* test result
