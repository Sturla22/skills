---
# Handoff 001: product-owner → workflow-architect

**Date:** 2026-03-21  
**From:** product-owner  
**To:** workflow-architect  
**Work ID:** expand-researcher-triggers

## Handoff rationale

This is a targeted operating-model edit. The change is small (one file, a few targeted insertions) but must be precise: the new trigger wording will be self-applied by future model instances, so vague or over-broad phrasing will fire the researcher too often; phrasing that is too narrow will reproduce the current miss.

## Canonical context

- Brief: `docs/work/expand-researcher-triggers/brief.md`
- Status: `docs/work/expand-researcher-triggers/status.md`
- File to edit: `AGENTS.md` (root)

## What changed since last checkpoint

Brief freshly written and approved by requester. No plan.md yet — workflow-architect should produce it inline or as a short rationale note before editing.

## Open question to resolve before editing

The brief names "Design cleanup" as one of the four skill sequences to add an optional `research` step. The trigger for that sequence would be: "when the pattern being cleaned toward has an external origin (a library API, a language-version idiom, a standard) not already verified in the codebase." Confirm this is intentional or substitute "Platform migration" (which more obviously references external MCU families). The brief intent is: cover the four sequences most likely to assume external facts. Resolve with your own judgment; no need to re-escalate to product-owner unless both options are equally risky.

## Requested next action

1. Produce a minimal diff of `AGENTS.md` that satisfies all four acceptance criteria in the brief:
   - Lower the `researcher` role trigger wording (role boundaries section)
   - Add one behavioral default naming the reactive trigger
   - Add an optional `research` step with a one-line trigger condition to each of the four named skill sequences
2. Keep all changes in `AGENTS.md` only unless you find a concrete reason CLAUDE.md must also change (document that reason).
3. Create `docs/workflow-experiments/EXP-002-expand-researcher-triggers.md` with: objective, evaluation window (next 5 tasks involving external components), and keep/revise/revert criteria.
4. Return a summary of changes and any residual risk to product-owner for final review before commit.

## Done-when criteria for this slice

- `researcher` role description trigger is reworded to fire reactively on external-component assumptions, not only on hard planning blockers.
- Four skill sequences each have an explicit optional `research` step with a trigger condition.
- One behavioral default added.
- Workflow experiment record created under `docs/workflow-experiments/`.
- No sequences that are purely internal (no external deps) were changed to make research mandatory.
- The brief's non-goals are respected: researcher stops before option comparison; no option surfacing added.
