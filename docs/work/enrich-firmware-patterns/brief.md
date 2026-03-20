# Brief: enrich-firmware-patterns

**Work ID:** enrich-firmware-patterns
**Date:** 2026-03-20
**Owner:** product-owner
**Classification:** workflow evolution / non-productized tool (repo skill enrichment)
**SemVer impact:** MINOR — adds guidance and examples to existing skills; no contract breakage

---

## Problem / desired outcome

The firmware skills in this repo (hardware-abstraction, simulation-harness-first, tdd, interface-contract-design, etc.) currently have thin or C-biased examples. They lack explicit guidance on well-established C++ embedded design patterns that practitioners reach for regularly.

**Desired outcome:** A durable, source-cited research summary of C++ embedded design patterns that can inform targeted skill updates — richer examples, better tooling references, and pattern-aware guidance in the right skills.

---

## Scope

Research the following named patterns plus related patterns the researcher finds commonly paired with them:

**Named patterns (seed list):**
- Active Object (asynchronous method execution via message queue)
- Ring buffer / circular buffer (lock-free and lock-based variants)
- ETL (Embedded Template Library) — what it provides and when to reach for it
- Placement new for memory-mapped peripherals (volatile, alignment, lifetime)
- State machine patterns (hierarchical, table-driven, std::variant-based)
- Command queue / message-passing between tasks
- Policy-based design (static polymorphism via templates as HAL alternative)
- CRTP (Curiously Recurring Template Pattern) for zero-cost abstractions
- Observer / event bus patterns without heap allocation

**Cast the net wider for:** any C++ embedded pattern that appears frequently in authoritative sources alongside the above.

---

## Non-goals

- Do not produce skill updates or implementation plans — that is planner's job after this
- Do not evaluate which MCU or RTOS platforms support each pattern — stay at the language/design level
- Do not compare vendor SDKs

---

## Acceptance criteria

- Research summary at `docs/work/enrich-firmware-patterns/evidence/research-cpp-embedded-patterns.md`
- Each pattern: definition, when to use, key tradeoffs, and at least one authoritative source citation
- Patterns that pair naturally are explicitly grouped or cross-referenced
- Gaps (patterns that need hardware-specific confirmation) are flagged
- Research boundary stated: where pattern facts end and skill-update decisions begin

---

## TDD expectation

Non-productized research task. No TDD. Verification: research summary exists, all patterns are cited, boundary is explicit.
