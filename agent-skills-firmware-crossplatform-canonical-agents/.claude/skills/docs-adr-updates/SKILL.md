---
name: docs-adr-updates
description: Keep README, architecture notes, and ADRs aligned with the implemented system. Use when updating documentation after a design change, writing a new ADR, recording a decision, or keeping docs in sync with code after a migration or refactor.
---

# Docs and ADR Updates

## Goal
Keep written design truth aligned with code.

## Use when
- a design decision changed
- an interface or failure mode changed materially
- a migration path was introduced

## Process
1. Read the existing docs and compare against the current code.
   ```
   grep -rn "TODO\|FIXME\|deprecated\|legacy" docs/ src/
   ```
2. Identify docs that are now stale or contradictory.
3. Update the minimum set needed to restore alignment.
4. Record important tradeoffs and implications.
5. Note migration and rollback concerns.

## Guardrails
- Do not update docs to match code that is itself wrong — fix the code first.
- ADR decisions are append-only — do not revise history; write a new ADR superseding the old one.
- Do not add docs for speculative or planned-but-unimplemented behavior.
- Every material interface change needs a corresponding doc or ADR update in the same PR.

## Failure Classification
- **Contradictory docs**: docs still describe the old behavior after update — re-read both and reconcile.
- **Missing decision record**: the reason for a major tradeoff is not captured — write or update the ADR.
- **Stale example**: a code example in the docs no longer compiles or runs — update or remove it.

## Output Contract
- docs updated
- stale assumptions removed
- decisions recorded
- migration notes
