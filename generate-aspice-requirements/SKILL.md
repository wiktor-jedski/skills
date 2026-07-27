---
name: generate-aspice-requirements
description: Generate software requirement specification according to ASPICE 4.0 process.
---

# Generate ASPICE Requirements
A generator for software requirement specification.

# OBJECTIVE
Transform high-level system requirements and stakeholder intent into a structured, analyzed, and traceable Software Requirements Specification (SRS).

# MANDATORY SYNTAX: EARS
You must write all functional requirements using the Easy Approach to Requirements Syntax (EARS):
- Ubiquitous: The [system name] shall [system response].
- Event-driven: WHEN [trigger], the [system name] shall [system response].
- State-driven: WHILE [state], the [system name] shall [system response].
- Unwanted Behavior: IF [unwanted condition], THEN the [system name] shall [system response].
- Optional: WHERE [feature is included], the [system name] shall [system response].

# REQUIRED ATTRIBUTES (ASPICE 17-54)
For every requirement, you must generate a Markdown metadata block containing:
- ID: [SW-REQ-XXX]
- Type: [Functional / Non-Functional (Performance, Safety, Security, etc.)]
- Priority: [High/Medium/Low]
- Feasibility: [Confirmed / Risk identified]
- Verification Criteria: [Brief description of how this will be tested in SWE.4]

# PROCESS WORKFLOW
1. DECOMPOSE: Break down the provided input into atomic software-level requirements.
2. ANALYZE: Evaluate each requirement for ambiguity, technical feasibility, and impact on the operating environment.
3. CATEGORIZE: Distinguish clearly between Functional and Non-Functional (Quality) requirements.
4. STANDARDIZATION: Rewrite them into the EARS syntax.
5. DOCUMENT: Assign a unique ID (e.g., SW-REQ-001) and output a valid Markdown SRS including a "Traceability Matrix" table.

# CONSTRAINTS
- NO AMBIGUITY: Avoid words like "fast," "easy," "user-friendly," or "optimized." Use quantitative values.
- NO DESIGN: Do not specify *how* to code it (e.g., "use a for-loop"). Specify *what* the software must do.
- DETERMINISM: If a requirement is missing context, you MUST stop and ask for clarification rather than hallucinating a solution.
- FORMAT: Use Markdown. Do NOT use JSON or code blocks for the requirements data. Use horizontal rules (`---`) to separate individual requirement cards.

# MARKDOWN OUTPUT STRUCTURE
For every requirement, you must use the following Markdown template:
---
## [SW-REQ-ID] [Title]
**Statement:** [Insert EARS Sentence Here]

| Attribute | Value |
| :--- | :--- |
| **Type** | (Functional / Performance / Safety / Security) |
| **Priority** | (High / Medium / Low) |
| **Feasibility** | (Feasible / High Risk / Needs Research) |
| **Verification** | (How to test this in SWE.4 - e.g., Unit Test / Integration Test) |

**Notes (optional):** [Technical dependencies or logic constraints]
---
