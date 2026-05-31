---
name: generate-aspice-architecture
description: Generate architectural design according to ASPICE 4.0 process.
---

# Generate ASPICE Architecture
A generator for software architectural design.

# OBJECTIVE
Design a stable, scalable, and traceable software architecture based on given documentation.
Decompose Software Requirements into Software Components and Interfaces.

# PROCESS GOALS (ASPICE 4.0)
1.  **Static Design:** Define software components, their boundaries, and external/internal interfaces.
2.  **Dynamic Design:** Describe how components interact (timing, concurrency, and states).
3.  **Resource Goals:** Define limits for CPU, Memory, or Network usage (if applicable).
4.  **Alternative Analysis:** You must justify your architectural choice against at least one alternative.
5.  **Traceability:** Every architectural element MUST trace back to one or more [SW-REQ-ID]s.

# ARCHITECTURAL GUIDELINES
- **Modularity:** Ensure high cohesion and low coupling.
- **No Detailed Design:** Focus on Software Patterns. No code/pseudocode. Stay at the "Component" level.
- **Safety/Security:** If a requirement is tagged "Safety," ensure the architecture includes mechanisms like "Input Validation" or "Redundancy."
- **Traceability:** If you create a component that doesn't link to a requirement, flag it as "Architectural Overhead."

# CONSTRAINTS
- Use Markdown headers and tables only.
- Do not generate code.
- If requirements are insufficient to define an interface, state: "INSUFFICIENT DATA FOR INTERFACE [Name]" at the top.

# MARKDOWN OUTPUT STRUCTURE
For every Architectural Component or Design Decision, use this format:

---
## [ARCH-ID] - [Component/Pattern Name]
**Description:** [High-level explanation of the component's responsibility]

| Attribute | Value |
| :--- | :--- |
| **Type** | (Module / Service / Interface / Middleware) |
| **Static Aspects** | (Defined Classes, Structs, or File Groups) |
| **Dependencies** | (Other ARCH-IDs or External Libraries) |
| **Traceability** | (Links to [SW-REQ-XXX] requirements) |

**Dynamic Behavior:**
- [Describe the execution flow, e.g., "Triggered by Interrupt," "Polled every 10ms," or "State-Machine based"]

**Interface Definition:**
- `Input`: [Data types and sources]
- `Output`: [Data types and destinations]

**Alternative Analysis (BP6):**
- *Chosen Approach:* [Reason for current design]
- *Alternative Considered:* [Description of a different way to build this]
- *Trade-off:* [Why the chosen approach is superior for this specific project]

**Resource Goals (optional):**
- *CPU*
- *Memory*
- *Network*
---
