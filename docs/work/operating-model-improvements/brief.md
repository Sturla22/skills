# Brief: Operating Model Improvements

**Work ID:** operating-model-improvements  
**Date:** 2026-03-23  
**Owner:** product-owner  
**Classification:** Non-productized tool (workflow / operating model)

---

## Problem / Desired Outcome

The operating model has gaps identified through two sources:

1. **Presentation research** — preparing the "AI for Firmware Engineers" talk surfaced patterns from the broader community (Ralph Loop, Grill Me, Karpathy's autoresearch, the skills ecosystem, context engineering as a named discipline) that are not reflected in the model.
2. **Reflex backport** — the `research` skill in `../reflex` was improved with structural durability guarantees ("write partial findings within first 3 tool uses") that have not been backported here.

The goal is a set of targeted, bounded improvements that raise the model to the current state of the art without over-engineering it.

---

## Scope

Nine concrete changes, each small and independently verifiable:

| # | Change | Surface |
|---|--------|---------|
| 1 | Add `story-loop` skill (Ralph pattern) — concrete instantiation of bounded-autonomy-loop | New skill |
| 2 | Add `grill-me` skill — structured brief/plan interrogation | New skill |
| 3 | Add `write-a-brief` skill — guided interview for medium/large briefs | New skill |
| 4 | Document three-tier skill model (canonical / team-installed / personal) | AGENTS.md |
| 5 | Backport `research` skill durability fix — write partial findings within first 3 tool uses + structured output file | `.agents/skills/research/SKILL.md` |
| 6 | Add "Context engineering" section to `docs/operating-model.md` | operating-model.md |
| 7 | Add Karpathy autoresearch pattern + AI-friendly code hypothesis to `workflow-evolution` skill | `.agents/skills/workflow-evolution/SKILL.md` |
| 8 | Add "why roles" rationale (2-3 sentences) before role definitions in AGENTS.md | AGENTS.md |
| 9 | Add agent failure note convention to AGENTS.md + operating-model.md | AGENTS.md, operating-model.md |

---

## Non-Goals

- Not changing the core role flow or role definitions
- Not adding new agent roles
- Not migrating to the `npx skills` install format (document it, don't require it)
- Not backporting anything else from reflex beyond the research skill fix

---

## Constraints

- Each change should be a PATCH or MINOR SemVer bump — no breaking contract changes
- Prefer the smallest diff per change
- New skills must follow the existing SKILL.md frontmatter format
- Changes to AGENTS.md must not break the `cli.py sync --check` validation

---

## Acceptance Criteria

1. `story-loop`, `grill-me`, and `write-a-brief` skills exist under `.agents/skills/` with correct frontmatter
2. `research` skill has "write partial findings within first 3 tool uses" as step 1
3. AGENTS.md has a "why roles" paragraph and a three-tier skill note
4. `operating-model.md` has a "Context engineering" section explaining the three layers
5. `workflow-evolution` skill mentions autoresearch pattern and AI-friendly code hypothesis
6. Agent failure note convention is documented in both AGENTS.md and operating-model.md
7. `python3 tools/cli.py sync --check` passes
8. CHANGELOG.md updated with all changes

---

## Assumptions / Open Questions

- The `grill-me` skill should be designed for both brief interrogation (product-owner) and plan stress-testing (planner) — same skill, same process, works in both contexts
- `write-a-brief` is modelled on Pocock's `write-a-prd` but adapted to our brief format, not GitHub issues
- The three-tier skill model is documentation only — no `cli.py` changes needed

---

## Code Drivers

- **Epistemic improvement** — research surfaced concrete patterns not yet in the model
- **Durability** — the research skill gap is a real operational risk (lost findings on session compaction)
- **Adoption** — naming "context engineering" helps adopters understand the system, not just copy its files
