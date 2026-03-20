# Handoff 002: product-owner → planner

**Work ID:** enrich-firmware-patterns
**From:** product-owner
**To:** planner
**Date:** 2026-03-20

---

## Canonical context

- Brief: `docs/work/enrich-firmware-patterns/brief.md`
- Research summary: `docs/work/enrich-firmware-patterns/evidence/research-cpp-embedded-patterns.md`
- Skills (canonical source): `.agents/skills/*/SKILL.md`
- Sync script: `scripts/sync_agent_layouts.py` — must be run after any skill edits to propagate changes to `.claude/skills/`, `.codex/`, `.github/` layouts

## What changed since the brief

Research is complete and requester-approved. 14 patterns are documented across 6 clusters:
1. Concurrency / message-passing: Active Object, ring buffer, command queue
2. Compile-time abstraction: CRTP, policy-based design
3. Heap-free library tooling: ETL
4. Hardware-interface construction: placement new for MMIO, RAII for peripheral ownership
5. Behavioral modeling: state machine variants (hierarchical, table-driven, std::variant)
6. Inter-component signaling: observer/event bus, delegate/callback wrapper

Surfaced extras beyond the seed list: memory pool, double buffer, ETL type-erasure interfaces.

## Key gaps from research (inform plan constraints)

- Lock-free ring buffer correctness is ISA-specific (Cortex-M0 caveat)
- ETL has no formal MISRA cert — flag when mentioning in safety contexts
- `std::variant` depends on toolchain version and exception config
- `volatile` alone insufficient for MMIO on multi-core/DMA — needs barrier note
- Active Object queue/stack sizing is workload-dependent

## Requested next action

Produce `docs/work/enrich-firmware-patterns/plan.md` covering:

1. Which existing skills should be updated and with what pattern content (map each pattern cluster to the most appropriate skill)
2. Whether any pattern warrants a new skill (e.g. a dedicated `active-object` or `state-machine` skill) vs. enriching an existing one
3. Ordered or parallel update lanes with explicit ownership boundaries
4. How to handle the research gaps (inline caveats in skill text, guardrails, or flag as out of scope)
5. Sync script requirement: each lane that edits skills must end with `python3 scripts/sync_agent_layouts.py`
6. Verification approach: structural check that each planned pattern appears in the target skill, no existing skill behavior is removed

## Constraints

- Canonical skill edits go in `.agents/skills/*/SKILL.md` only — sync propagates to other layouts
- Prefer enriching existing skills over creating new ones unless the pattern genuinely has no good home
- Keep each skill focused — do not dump all 14 patterns into one skill
- Prefer the smallest useful diff per skill

## Done-when (for planner)

- `plan.md` maps each pattern to a target skill with rationale
- Parallel vs. serial lanes are explicit with ownership boundaries
- Sync step is named in each lane
- Verification expectations are stated
- Any new-skill proposals are justified against the existing skill set
