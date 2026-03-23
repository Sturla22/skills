---
name: design-an-interface
description: Generate three or more radically different interface designs in parallel using the Design It Twice methodology, then compare and recommend the deepest option. Use when implementing a new module, HAL boundary, or API surface where the interface shape will be hard to change later.
allowed-tools: Read, Grep, Glob, Bash
---

# Design an Interface

Implements "Design It Twice" from John Ousterhout's "A Philosophy of Software Design." Generate multiple radically different interfaces so the best can be chosen deliberately rather than defaulting to the first idea.

## Principle

A deep module has a small interface hiding large implementation. A shallow module has a large interface with little substance. Always prefer deep. The goal of this skill is to make the depth tradeoff explicit.

## Process

### Step 1 — Gather requirements

Understand before designing:
- The problem domain and what callers need to do
- The key operations (not the implementation)
- What must stay internal vs. what must be exposed
- Known constraints: ISR-safe, no heap, latency budget, thread ownership, error handling expectations
- Whether the interface will be mocked or faked in tests — this constrains size and purity

### Step 2 — Generate designs in parallel

Spawn 3+ sub-agents (or work through each design in sequence if sub-agents are not available), each with a different design constraint:

- **Design A — Minimal:** minimize the number of functions (1–3 max). Force hidden complexity.
- **Design B — Flexible:** maximize caller flexibility and composability.
- **Design C — Common-case optimized:** optimize the interface for the single most common usage pattern.
- **Design D (optional) — Pattern-driven:** apply a specific architectural pattern (ports and adapters, actor model, command/query separation, etc.).

Each design must produce:
- Function signatures (with types and units in names or comments)
- A usage example showing the most common case
- What complexity it hides from callers
- Trade-off notes (what becomes harder with this design)

### Step 3 — Present designs

Show each design sequentially. For each: signatures, usage example, what it hides, trade-offs.

Do not evaluate yet. Present first.

### Step 4 — Compare

Evaluate all designs on:
- Interface simplicity (fewer functions, simpler parameters)
- Generality (handles the known cases without special-casing)
- Implementation depth (how much complexity does the interface hide?)
- Fit for stated constraints (ISR-safe, testable, latency, heap policy)

Give an opinionated recommendation. Name one design as the default choice and explain why. Call out the runner-up.

### Step 5 — Synthesize

Identify whether the best design is one of the generated options or a useful hybrid. Note any durable design decisions for the work packet (suitable for a brief or ADR).

## Guardrails

- Enforce radical differences between designs — if two designs look similar, one is a variation, not an alternative. Make it more extreme.
- Focus on interface shape only in steps 2–3. Skip implementation details.
- Do not select a design without presenting the trade-offs.
- Do not produce a design where the interface mirrors the hardware register map or internal state — that is shallow by construction.
- Do not skip the recommendation — presenting options without a recommendation transfers the decision cost to the caller without reducing it.

## Done-when

- Three or more genuinely different designs have been presented.
- Each design has signatures, a usage example, what it hides, and trade-offs.
- A recommendation has been made with reasoning.
- Any durable design decisions are noted for the work packet.

## Output

- Design options (A, B, C, D) with signatures, examples, hidden complexity, and trade-offs
- Comparison across simplicity, generality, depth, and constraints
- Opinionated recommendation with reasoning
- Durable design decisions for work packet
