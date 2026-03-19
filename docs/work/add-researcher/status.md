# Status: add-researcher

**Work ID:** add-researcher
**Last updated:** 2026-03-19
**Current owner:** product-owner
**State:** complete

---

## Current state

All acceptance criteria met. Implementation committed.

## Changes made

| File | Action |
|------|--------|
| `.claude/agents/researcher.md` | Created — new optional specialist role |
| `.claude/skills/research/SKILL.md` | Created — new research skill |
| `AGENTS.md` | Updated — researcher in optional specialists, role flow #11, external domain investigation skill sequence |
| `.claude/CLAUDE.md` | Updated — researcher delegation trigger in Working rules |
| `CHANGELOG.md` | Updated — Added entries for role, skill, skill sequence |
| `docs/work/add-researcher/brief.md` | Created — canonical brief |
| `docs/work/add-researcher/status.md` | Created — this file |

## Acceptance criteria check

- [x] `.claude/agents/researcher.md` exists with correct frontmatter, use-when, responsibilities, return contract
- [x] `.claude/skills/research/SKILL.md` exists with structured process and research-boundary guardrail
- [x] `AGENTS.md` lists researcher in optional specialists with boundary description
- [x] `AGENTS.md` includes researcher in default role flow as entry #11
- [x] `AGENTS.md` includes External domain investigation skill sequence
- [x] `.claude/CLAUDE.md` includes researcher delegation trigger
- [x] `CHANGELOG.md` has Added entries for role, skill, and skill sequence
- [x] No existing role, skill, or template was modified

## Residual risk

The researcher/planner boundary is the sharpest design risk. If the `research` skill's process steps creep into option-comparison or task-framing in practice, the boundary will erode. The guardrails section of `SKILL.md` addresses this explicitly. Monitor across the next 2–3 work packets that involve external domain investigation.

**What was not verified:** behavior on real hardware (not applicable — this is a workflow addition). Skill triggering accuracy depends on model interpretation of the description frontmatter; adjust if the skill fires inappropriately or fails to fire when needed.
