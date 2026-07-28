---
name: doc-architecture
description: Generate and maintain a canonical architecture document. Use when the user wants to define, compare, record, review, or update project architecture.
---

# Document Architecture

Create and maintain `docs/architecture.md`.

The document specifies the current architecture. Use stable `ARCH-*` identifiers for normative architecture elements.

Use short sentences, active voice, and consistent terms. Apply ASD-STE100 principles. Do not claim formal conformance.

## Process

### 1. Get context

Read:

- The current conversation
- `docs/requirements.md`
- `docs/architecture.md`, if it exists
- Applicable `CONTEXT.md` files and ADRs
- Applicable code, if code exists

Run `/codebase-design`. Use its terms for modules, interfaces, seams, adapters, depth, leverage, and locality.

Report conflicts between documents and code. Ask the user to resolve each conflict.

This step is complete when the active requirements, current architecture, and source conflicts are clear.

### 2. Resolve decision gaps

Check:

- Module responsibilities and seams
- Interfaces
- Collaborations and runtime behavior
- Data ownership and flow
- Deployment
- Performance and resource limits
- Safety, security, and reliability
- Verification at architecture seams

If a missing decision changes the architecture, give the user a short interview agenda. Ask the user to start `/grill-with-docs`. Stop this skill.

This step is complete when the constraints are clear enough to compare architecture options.

### 3. Compare options

Use Design It Twice from `/codebase-design` for each new or materially changed architecture choice. Produce at least three materially different options.

Compare requirement coverage, module depth, seam placement, locality, runtime behavior, quality effects, and reversibility.

Recommend one option or one explicit hybrid. Wait for the user to select the architecture.

Skip this step for settled choices, wording changes, and traceability updates.

This step is complete when the user selects one option.

### 4. Draft the change set

Use these element types:

- `Module`
- `Interface`
- `Collaboration`
- `Data`
- `Deployment`
- `Mechanism`

Every active element requires:

- ID and title
- Type and status
- Active `REQ-*`, or an architecture-overhead reason
- Dependencies, including `None`
- Responsibility

Add the required content for its type:

- `Module`: contract
- `Interface`: contract
- `Collaboration`: participants and runtime behavior
- `Data`: owner, semantic or structure contract, and flow
- `Deployment`: placement and runtime constraints
- `Mechanism`: behavior and applicable quality constraints

Add resource limits only when a source specifies them. Add an ADR link only when an ADR exists.

Use `/domain-modeling` to offer an ADR when a choice is hard to reverse, surprising without context, and based on a real trade-off. Keep decision rationale and rejected alternatives in the ADR.

Show the proposed additions, changes, and deprecations. Wait for explicit approval.

This step is complete when the user approves the full change set.

### 5. Update the document

Create `docs/architecture.md` if it does not exist. Add a short system overview before the element cards.

Make a surgical update:

- Preserve unaffected text, order, and IDs.
- Keep an ID when its meaning does not change.
- Create a new ID when meaning changes.
- Continue after the highest existing number.
- Keep deprecated elements in place.
- Give each deprecated element a reason and replacement ID, if one exists.

Use this base card:

```markdown
## ARCH-001 — <Element name>

| Attribute | Value |
| --- | --- |
| Type | Module / Interface / Collaboration / Data / Deployment / Mechanism |
| Status | Active / Deprecated |
| Requirements | REQ-001, or Architecture overhead: <reason> |
| Dependencies | ARCH-002, external system, or None |
| ADR | <Link, or omit this row> |

**Responsibility:** <One clear responsibility.>

<Add the required type-specific content.>
```

Use a Mermaid diagram only when it makes a relationship, sequence, state, or deployment easier to understand.

This step is complete when every approved architecture element is in the document.

### 6. Verify requirement coverage

Maintain one coverage table in `docs/architecture.md`. Include every active `REQ-*`.

Map each requirement to one or more `ARCH-*`. Use `No architecture impact` with a reason when applicable. Treat `Unresolved` as incomplete work.

Each active `ARCH-*` must trace to an active `REQ-*` or state its architecture-overhead reason.

This step is complete when every active requirement and architecture element has resolved traceability.

## Completion gate

The architecture document is complete when:

- Every active `REQ-*` has resolved architecture coverage.
- Every active `ARCH-*` has the required common and type-specific content.
- Every interface and collaboration has enough detail for verification.
- Every approved change is present.
- No unapproved normative change is present.
