# SWE.5 Integration Testing Checklist

Use this checklist before marking any SWE.5 obligation or SWE.5 task as complete.

If any mandatory item fails, the obligation is not complete.

---

# Section 1 - Architecture Verification

## Mandatory

* [ ] The obligation is traceable to an ARCH-* component.
* [ ] The obligation references at least one SW-REQ-*.
* [ ] The obligation describes architectural behavior.
* [ ] The obligation is not merely validating a single function or method.

Reject completion if:

```text
The obligation can be satisfied by testing one isolated class with all dependencies mocked.
```

That is usually SWE.4, not SWE.5.

---

# Section 2 - Integration Scope

## Mandatory

* [ ] The System Under Test is identified.
* [ ] At least two collaborating software units participate.
* [ ] Architectural interactions are exercised.
* [ ] Data is exchanged across unit boundaries.

Examples of valid integration scope:

* SceneRouter + SaveManager
* SaveManager + SaveContracts
* GameState + SaveContracts
* Scene Controller + GameState

Examples of invalid integration scope:

* RuntimeStateModels only
* SaveManager only
* One helper class only

---

# Section 3 - Real Components

## Mandatory

* [ ] Real implementations are used where practical.
* [ ] Test doubles exist only at architecture boundaries.
* [ ] The test does not mock every dependency.

Reject completion if:

```text
All collaborating units are mocked.
```

or

```text
The test only verifies method calls on mocks.
```

---

# Section 4 - Architectural Behavior

## Mandatory

The test demonstrates at least one of:

* [ ] Architectural sequence.
* [ ] Architectural state transition.
* [ ] Architectural data flow.
* [ ] Architectural failure handling.
* [ ] Architectural recovery behavior.

Examples:

* checkpoint written before route opens
* save failure activates lock
* retry reuses frozen payload
* restore loads correct route

---

# Section 5 - Evidence Quality

## Mandatory

The test verifies observable outcomes.

* [ ] State changes are verified.
* [ ] Returned results are verified.
* [ ] Produced contracts or payloads are verified.
* [ ] Architectural side effects are verified.

Reject completion if:

```text
Only mock interactions are verified.
```

without verifying architectural results.

---

# Section 6 - Robustness Coverage

## Recommended

For each architecture component verify:

* [ ] Nominal path
* [ ] Failure path
* [ ] Recovery path

Examples:

| Component   | Failure Example    | Recovery Example      |
| ----------- | ------------------ | --------------------- |
| SceneRouter | Save failure       | Retry succeeds        |
| SaveManager | Corrupt save       | Recovery save created |
| GameState   | Invalid checkpoint | Fresh initialization  |

---

# Section 7 - Obligation Coverage

## Mandatory

* [ ] Every obligation is referenced by at least one test.
* [ ] Every test references at least one obligation.
* [ ] Obligation IDs appear in test traceability comments.

Required format:

```csharp
/// Verifies IT-ARCH-002-001
/// Verifies ARCH-002
/// Traces SW-REQ-012
```

---

# Section 8 - SWE.4 Leakage Check

## Mandatory

Reject completion if any statement is true:

* [ ] Test only verifies validation logic.
* [ ] Test only verifies bounds checking.
* [ ] Test only verifies one method.
* [ ] Test only verifies one unit.
* [ ] Test behavior already fully covered by unit tests.

If yes:

```text
Move verification to SWE.4.
```

---

# Section 9 - Completion Decision

## SWE.5 Obligation Complete

All mandatory items pass.

## SWE.5 Task Complete

* [ ] All obligations implemented.
* [ ] All tests passing.
* [ ] Traceability complete.
* [ ] Checklist passed for every obligation.

Only then may the task be marked PASSED.

---

# Final Sanity Question

Ask:

```text
If every collaborator except one were replaced by mocks,
would this test still pass?
```

If the answer is:

```text
Yes
```

the test is probably not a real integration test.

Review the obligation again before closing it.
