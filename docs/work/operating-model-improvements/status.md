# Status: Operating Model Improvements

**Updated:** 2026-03-23
**Current owner:** product-owner
**State:** Complete — pending final commit

---

## Current state

All nine changes implemented and verified. `tools/cli.py sync --check` passes (79 files, hash 808e252fc7e8). CHANGELOG.md updated. Status updated. Ready to commit.

## Completed work

- **Commit A scope** — New skills created: `story-loop`, `grill-me`, `write-a-brief`, `design-an-interface`, `ubiquitous-language`
- **Commit B scope** — Updated: `research` skill (partial-findings durability), `tdd` skill (Step 0, slice anti-pattern, per-cycle checklist, mocking guardrail, REFERENCE.md), `workflow-evolution` skill (autoresearch pattern, AI-friendly code structure hypothesis), `AGENTS.md` (why-roles rationale, skill tiers), `docs/operating-model.md` (context engineering, agent failure notes)
- **Commit C scope** — CHANGELOG.md updated, sync verified

## Next action

Commit all changes. Work complete.

## Decisions made

| # | Decision |
|---|----------|
| 1 | Keep `bounded-autonomy-loop` as safety contract; `story-loop` is the concrete instantiation |
| 2 | `grill-me` serves both product-owner and planner — one skill, both contexts |
| 3 | `write-a-brief` targets our `brief.md` format, not GitHub issues |
| 4 | Three-tier skill model is documentation only — no `cli.py` changes |
| 5 | Research durability fix is a backport from reflex (write partial findings within first 3 tool uses) |
| 6 | Autoresearch pattern goes in `workflow-evolution` skill as an optimization loop note |
| 7 | Agent failure note is a lightweight convention, no new template needed |

## Blocking items

None.
