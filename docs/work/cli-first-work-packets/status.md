# Work Status

## Storage

- Work ID: `cli-first-work-packets`
- File path: `docs/work/cli-first-work-packets/status.md`
- Brief: `docs/work/cli-first-work-packets/brief.md`
- Plan: `docs/work/cli-first-work-packets/plan.md`

## Current owner

- Role: product-owner
- Date: 2026-04-07
- Lane: closed
- Worktree / isolation: primary working tree

## Current summary

Confirmed that `tools/cli.py` already provides the supported CLI surface for work-packet scaffolding and inspection. The remaining gap is guidance strength: the repo contract did not yet say strongly enough that supported CLI operations should be used before hand-creating packet artifacts.

## Current step

Closed.

## Last completed checkpoint

- Created the canonical work packet with `python3 tools/cli.py new-work cli-first-work-packets`
- Updated the shared workflow docs, Copilot instructions, README, and changelog to encode a CLI-first rule
- Added the workflow experiment record for evaluating the change
- Verified the packet with `python3 tools/cli.py check-work cli-first-work-packets`

## Open blockers

- None

## Active risks / unknowns

- The rule must remain narrow enough that direct edits to scaffolded content are still clearly allowed

## Continuous V&V status

- Verification: packet scaffold confirmed via `tools/cli.py`; docs surfaces updated; `python3 tools/cli.py check-work cli-first-work-packets` passed
- Validation: not applicable for this docs-only workflow clarification
- Integration: not applicable
- Open gaps: none for this docs-only slice

## Next action

None — work is complete.

## Active evidence

- Verification: `docs/work/cli-first-work-packets/evidence/cli-surface-baseline.md`, `docs/workflow-experiments/EXP-008-cli-first-work-packets.md`
- Hypotheses: stronger CLI-first guidance is enough; no tooling change is needed
- Optimization scorecard:
- Recent handoff:
