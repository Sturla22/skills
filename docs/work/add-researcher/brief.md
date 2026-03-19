# Brief: add-researcher

**Work ID:** add-researcher
**Date:** 2026-03-19
**Owner:** product-owner
**Classification:** workflow evolution (non-productized tool / repo contract addition)
**SemVer impact:** MINOR — adds new optional role name and skill name to the public contract; no existing users break

---

## Problem / desired outcome

There is a class of work the current model absorbs poorly: external domain investigation that must happen **before planning is even possible**. Examples: datasheet synthesis, standards/spec reading, errata hunting, technology landscape surveys, feasibility signals from external sources.

Currently this falls informally to `planner` or `product-owner`, which either creates a hidden planning bottleneck or gets done sloppily without a durable artifact. The result is plans built on unverified external facts, or repeated re-research when the same domain comes up in future work.

**Desired outcome:** a named, bounded `researcher` role and companion `research` skill that close a specific external knowledge gap and produce a durable, source-cited summary — then stop before option comparison or design begins.

---

## Scope

- Create `.claude/agents/researcher.md`
- Create `.claude/skills/research/SKILL.md`
- Update `AGENTS.md`: add researcher to optional specialists and default role flow; add external domain investigation skill sequence
- Update `.claude/CLAUDE.md`: add researcher delegation trigger (mirrors technical-writer / release-manager pattern)
- Update `CHANGELOG.md`: add entries under `[Unreleased] → Added`

## Non-goals

- Modifying any existing role or skill
- Adding planning, option comparison, or design decision logic to the researcher role
- Requiring researcher on all feature work (it is optional, triggered only when an external knowledge gap blocks planning)

---

## Constraints

- Researcher/planner boundary must be explicit and sharp: researcher stops at facts, planner starts at options
- All findings must be source-cited with title, version, section, and retrieval date
- The role must fit the existing optional-specialist pattern (returns to product-owner, not directly to requester)
- No new templates required for this addition

---

## Acceptance criteria

1. `.claude/agents/researcher.md` exists with correct frontmatter, use-when triggers, responsibilities, and return contract
2. `.claude/skills/research/SKILL.md` exists with a structured process that enforces the research-boundary guardrail
3. `AGENTS.md` lists `researcher` in optional specialists with a one-line boundary description
4. `AGENTS.md` includes `researcher` in the default role flow as entry #11
5. `AGENTS.md` includes an `External domain investigation` skill sequence
6. `.claude/CLAUDE.md` includes a researcher delegation trigger in Working rules
7. `CHANGELOG.md` has entries under `[Unreleased] → Added` for the role, skill, and skill sequence
8. No existing role, skill, or template is modified

---

## Assumptions / open questions

- The researcher/planner boundary is the sharpest design risk. If the research skill's process steps creep into option-comparison or task-framing, the boundary will erode in practice. The guardrails section must be explicit.
- No workflow experiment record is needed for this addition because the role fills a clearly named gap that has been observed repeatedly (datasheet/spec work, standards reading) and the intervention is fully reversible (adding optional files).

---

## TDD expectation

This is a non-productized workflow tool (docs and prompt files). TDD is not applicable. Verification is structural: check that all files exist, all acceptance criteria above are satisfied, and no existing files are modified.
