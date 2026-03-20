# Handoff 003: product-owner → developer (lanes A, B, C, E)

**Work ID:** enrich-firmware-patterns
**From:** product-owner
**To:** developer (four parallel lanes)
**Date:** 2026-03-20

---

## Canonical context

- Brief: `docs/work/enrich-firmware-patterns/brief.md`
- Plan: `docs/work/enrich-firmware-patterns/plan.md`
- Research: `docs/work/enrich-firmware-patterns/evidence/research-cpp-embedded-patterns.md`

## What changed since planning

- Q1 resolved: `firmware-migration` is out of scope. The 5-skill mapping in plan section 5 is final.
- Step 0 (sync script baseline) passed: exits 0 on current tree.

## Lane ownership

| Lane | Target skill | Patterns |
|---|---|---|
| A | `.agents/skills/hardware-abstraction/SKILL.md` | Policy-based design, CRTP, placement new for MMIO, RAII for peripheral ownership |
| B | `.agents/skills/simulation-harness-first/SKILL.md` | Active Object, command queue, ETL, HSM |
| C | `.agents/skills/tdd/SKILL.md` | Ring buffer/SPSC, table-driven FSM, std::variant FSM |
| E | `.agents/skills/resource-budget-review/SKILL.md` | Memory pool, double buffer, AO queue/stack sizing |

## Constraints (all lanes)

- Canonical edits to `.agents/skills/*/SKILL.md` only
- Smallest useful diff — additions only, zero deletions of existing content
- Each lane ends with `python3 scripts/sync_agent_layouts.py` and confirms exit 0
- Required wording for guardrails and gap notes is specified in plan.md per lane

## Done-when (all lanes)

See plan.md section 7 per-lane done-when criteria and section 8 structural verification checklist.
Lane D (interface-contract-design) follows after lanes A, B, C, E are merged.
