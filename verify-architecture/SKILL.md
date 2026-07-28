---
name: verify-architecture
description: Verify architecture with integration, contract, or smoke tests. Use when the user wants to plan, implement, review, or trace architecture verification, including ASPICE SWE.5 work.
---

# Verify Architecture

Verify observable behavior across architecture seams. Maintain the verification documents in `docs/testing/architecture/`.

Use short sentences, active voice, and consistent terms in all documents. Apply ASD-STE100 principles. Do not claim formal conformance.

## Process

### 1. Get context

Read:

- `docs/requirements.md`
- `docs/architecture.md`
- Applicable ADRs and `CONTEXT.md`
- `docs/testing/architecture/index.md`, if it exists
- Applicable obligation files, code, and tests

Report conflicts between documents and code. Ask the user to resolve each conflict.

If an `ARCH-*` entry does not specify enough behavior for verification, keep its coverage open. Ask the user to run `/doc-architecture`. Stop this skill.

This step is complete when each applicable architecture seam and its expected behavior are clear.

### 2. Draft coverage and obligations

Classify every active `ARCH-*`:

- `Open` when verification work remains.
- `Closed` when passing evidence exists or the element has no observable integration behavior.

For a closed element with no verification impact, record the reason.

Create one obligation for one observable architecture behavior. Derive each obligation from active `ARCH-*` and `REQ-*` content. Add failure, recovery, timing, security, or resource obligations only when the source documents specify them.

Use stable `AV-ARCH-001-001` IDs. Preserve an ID while its meaning stays the same.

Show the proposed index and obligation changes. Wait for explicit approval.

This step is complete when the user approves the full change set.

### 3. Update verification documents

Create `docs/testing/architecture/index.md` if it does not exist. Include every active `ARCH-*`:

```markdown
| Architecture | Status | Evidence |
| --- | --- | --- |
| ARCH-001 | Open / Closed | AV-ARCH-001-001, test name, or no-impact reason |
```

Create or update `docs/testing/architecture/<ARCH-ID>.md` for each applicable architecture element. Use [templates/obligation.md](templates/obligation.md).

Use `Open` when evidence is missing. Use `Closed` when passing evidence exists. If an obligation is superseded, close it and record the reason and replacement ID.

Make surgical updates. Preserve unaffected text, order, and IDs.

This step is complete when the approved changes are in the index and obligation files.

### 4. Implement evidence when requested

Select the evidence form that matches the seam:

- Use an integration test for in-process modules.
- Use a contract test for remote or external interfaces.
- Use a smoke test for deployment or startup behavior.

Use real collaborating modules for in-process seams. Use a representative adapter for a remote or external seam. Put test doubles outside the behavior under verification.

Verify observable results across the seam. Reference the applicable `AV-ARCH-*` ID in the test name, annotation, or nearby comment.

Run the applicable tests.

This step is complete when each implemented test passes and supplies evidence for its obligation.

### 5. Close verified work

Close an obligation only when its evidence passes. Record the test name or other durable evidence identifier.

Close an index row only when all applicable obligations are closed or the row has an approved no-impact reason.

Report open rows and failed evidence to the user.

This step is complete when the index shows the current verification state.

## Completion gate

Architecture verification is complete when:

- Every active `ARCH-*` has a closed index row.
- Every applicable behavior has an obligation.
- Every obligation traces to an active `ARCH-*` and its applicable active `REQ-*`.
- Every test references an `AV-ARCH-*` obligation.
- Evidence crosses the selected seam and verifies an observable result.
- All required evidence passes.
