---
name: doc-requirements
description: Generate and maintain a canonical requirements document. Use when the user wants to define, formalize, review, or update project requirements.
---

# Document Requirements

Create and maintain `docs/requirements.md`.

The document is the source of truth for project requirements. Use stable `REQ-*` identifiers.

## Process

### 1. Get context

Read these sources:

- The current conversation
- `docs/requirements.md`, if it exists
- The applicable `CONTEXT.md`
- The applicable ADRs
- The applicable code, if code exists

Use the terms from `CONTEXT.md`.

Compare the sources. Report each contradiction to the user. Ask the user to resolve each contradiction before you change the document.

This step is complete when you know the current requirements and all source contradictions are visible to the user.

### 2. Find decision gaps

Check these subjects:

- Required behavior
- Boundary conditions
- Error behavior
- Operating conditions
- Performance
- Safety
- Security
- Reliability
- Usability and accessibility
- Compatibility
- Verification

Separate a missing fact from a missing decision. Get facts from the project sources. Ask the user to make decisions.

If a missing decision can materially change a requirement, give the user a short interview agenda. Ask the user to start `/grill-with-docs`. Stop this skill. Run this skill again after the interview.

Use `TBD` only when the missing detail cannot change the meaning of the requirement.

This step is complete when each material decision is resolved.

### 3. Draft the change set

Write each requirement as one atomic and verifiable statement.

Use EARS for behavior:

- Ubiquitous: The `<system>` shall `<response>`.
- Event: WHEN `<trigger>`, the `<system>` shall `<response>`.
- State: WHILE `<state>`, the `<system>` shall `<response>`.
- Unwanted event: IF `<condition>`, THEN the `<system>` shall `<response>`.
- Optional feature: WHERE `<feature is present>`, the `<system>` shall `<response>`.

Use a measurable `shall` statement for a quality requirement or a constraint. Do not add an EARS condition when it does not add information.

Use one of these types:

- `Behavior` for a required action or result
- `Quality (<characteristic>)` for a measurable property
- `Constraint` for a mandatory limit on the solution or its operating environment

For each verification, specify the method and the observable pass condition.

Show the proposed additions, changes, and deprecations to the user. Wait for explicit approval.

This step is complete when the user approves the full change set.

### 4. Update the document

Create `docs/requirements.md` if it does not exist.

Make a surgical update:

- Preserve unaffected text and order.
- Preserve the meaning of each existing ID.
- Keep the ID when wording changes but meaning does not change.
- Create a new ID when meaning changes.
- Continue after the highest existing number.
- Mark a removed requirement as `Deprecated`.
- Give the deprecation reason and replacement ID, if one exists.

Use this format for each requirement:

```markdown
## REQ-001 — <Title>

**Statement:** <Atomic requirement statement>

| Attribute | Value |
| --- | --- |
| Type | Behavior / Quality (<characteristic>) / Constraint |
| Status | Active / Deprecated |
| Verification | <Method and observable pass condition> |

**Notes:** <Only necessary constraints or clarifications. Omit when empty.>
```

Do not add feasibility or priority. Do not add artificial source IDs. Do not add an architecture traceability matrix.

This step is complete when every approved change is in `docs/requirements.md` and every active requirement has a verification pass condition.

## Completion check

Before you finish, confirm all of these results:

- Each active requirement has one stable `REQ-*` ID.
- Each statement is atomic and unambiguous.
- Each quality statement is measurable.
- Each verification has a method and an observable pass condition.
- Each deprecated requirement has a reason.
- Each approved change is present.
- No unapproved normative change is present.
