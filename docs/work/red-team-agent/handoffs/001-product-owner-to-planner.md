# Handoff

## Storage

- Work ID: `red-team-agent`
- File path: `docs/work/red-team-agent/handoffs/001-product-owner-to-planner.md`
- Packet root: `docs/work/red-team-agent/`

## From

- Agent: product-owner
- Date: 2026-03-20

## To

- Agent: planner

## Handoff rationale

Brief is complete and all decisions are locked. No open questions remain.
Planner sequences the deliverables and writes `plan.md` before implementation starts.

## Canonical context

- Brief: `docs/work/red-team-agent/brief.md`
- Plan: `docs/work/red-team-agent/plan.md` _(to be written)_
- Status: `docs/work/red-team-agent/status.md`
- Evidence touched: none yet

## Delta since last checkpoint

- What changed: brief written from scratch
- New decisions: all locked in brief (see §Assumptions, §Constraints, §In scope)
- New or changed assumptions: none
- New or changed risks / blockers: none
- Files or artifacts added / updated: `brief.md`, `status.md`, this handoff

## Context the recipient must preserve

- `red-team` fires after `planner` writes `plan.md`, before `developer` starts — plan-time only
- Must be clearly distinguished from `reviewer` (which fires post-implementation)
- Findings go in a separate document (`evidence/red-team-findings.md`), not inline in `plan.md`
- Returns findings to `product-owner` with one of: approve / revise / escalate
- Medium/high-risk work only; risk level is a product-owner/planner judgment call in v1
- Non-productized tool — no TDD, manual verification against ACs is sufficient

## Parallel work context

- Lane / owner: single lane
- Dependencies: none
- Integration checkpoint: `plan.md` returned to product-owner for approval before implementation

## Evidence gathered so far

None.

## Impact analysis / downstream effects

- `AGENTS.md` public contract adds one new optional specialist — MINOR SemVer
- No existing role renames or removals

## Requested next action

1. Review `brief.md` — confirm all ACs are implementable as stated
2. Sequence the deliverables (agent TOML, skill, findings template, AGENTS.md, CLAUDE.md, sync, changelog)
3. Identify any ordering constraints between deliverables
4. Write `plan.md`
5. Return to product-owner for approval before implementation starts

## Done-when

`plan.md` exists with ordered steps, each step has clear acceptance criteria,
and product-owner has approved before a developer starts.
