# Handoff

## Storage

- Work ID: `red-team-agent`
- File path: `docs/work/red-team-agent/handoffs/002-product-owner-to-developer.md`
- Packet root: `docs/work/red-team-agent/`

## From

- Agent: product-owner
- Date: 2026-03-20

## To

- Agent: developer

## Handoff rationale

`plan.md` is complete, no open questions remain, and the work is small enough
for a single developer lane to implement directly.

## Canonical context

- Brief: `docs/work/red-team-agent/brief.md`
- Plan: `docs/work/red-team-agent/plan.md`
- Status: `docs/work/red-team-agent/status.md`
- Evidence touched: none yet

## Delta since last checkpoint

- What changed: `plan.md` written and approved for execution
- New decisions: none beyond the approved plan
- New or changed assumptions: none
- New or changed risks / blockers: preserve unrelated `AGENTS.md` edits; make the `red-team` vs `reviewer` boundary explicit in both roles
- Files or artifacts added / updated: `plan.md`, `status.md`, this handoff

## Context the recipient must preserve

- `red-team` is a pre-implementation adversarial review role for medium/high-risk work only
- Findings are structured and separate from `plan.md`
- Findings return to `product-owner` with exactly one recommendation: approve, revise, or escalate
- `reviewer` remains the post-implementation patch/plan critic and must stay distinct
- This is a non-productized tool change; verification is manual AC inspection plus `scripts/cli.py sync --check`

## Parallel work context

- Lane / owner: single lane / developer
- Dependencies: none
- Integration checkpoint: run sync, verify ACs, then return packet for verification/review

## Evidence gathered so far

- `brief.md` and `plan.md` define the accepted scope, constraints, and ACs

## Impact analysis / downstream effects

- Adds one optional specialist role and one reusable skill/template set
- Changes the documented repo contract in a backward-compatible way
- Requires synced generated agent outputs under Claude/GitHub/Codex target paths

## Requested next action

1. Implement the new source files and doc updates from `plan.md`
2. Run `scripts/cli.py sync` and `scripts/cli.py sync --check`
3. Confirm AC-001 through AC-007 by inspection
4. Update `status.md` with verification state and hand back to product-owner

## Done-when

All planned files are implemented, sync is clean, and the packet is ready for
verification against the accepted criteria.
