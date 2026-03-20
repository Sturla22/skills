# Handoff 001: product-owner → researcher

**Work ID:** enrich-firmware-patterns
**From:** product-owner
**To:** researcher
**Date:** 2026-03-20

---

## Canonical context

- Brief: `docs/work/enrich-firmware-patterns/brief.md`
- Output target: `docs/work/enrich-firmware-patterns/evidence/research-cpp-embedded-patterns.md`

## Research question

What are the well-established C++ embedded design patterns that firmware practitioners reach for regularly, what are their tradeoffs, and which authoritative sources describe them?

Seed patterns: Active Object, ring buffer (lock-free and lock-based), ETL (Embedded Template Library), placement new for MMIO peripherals, state machine variants (hierarchical / table-driven / std::variant), command queue / message-passing, policy-based design, CRTP for zero-cost abstractions, observer/event bus without heap allocation.

Cast wider: surface any patterns that appear frequently alongside the above in authoritative sources.

## What changed

New work packet. No prior research exists.

## Requested next action

Produce `docs/work/enrich-firmware-patterns/evidence/research-cpp-embedded-patterns.md` per the brief's acceptance criteria. Return the path, an executive summary, gaps, and the explicit research boundary.

## Done-when

- Each named pattern has: definition, when to use, key tradeoffs, at least one authoritative citation
- Naturally paired patterns are grouped or cross-referenced
- Gaps requiring hardware or platform confirmation are listed
- Research boundary sentence is present
