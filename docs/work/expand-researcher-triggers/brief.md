# Brief: expand-researcher-triggers

**Work ID:** expand-researcher-triggers
**Date:** 2026-03-21
**Owner:** product-owner
**Delivery class:** Non-productized workflow change
**Status:** Brief approved — awaiting plan

## Problem / desired outcome

The `researcher` role trigger in AGENTS.md is set too high. The current wording — "when a knowledge gap must be closed before planning is possible" — implies a hard blocker. In practice, work that references external components (MCU families, SDKs, vendor libraries, or standards) often proceeds with local-disk search as a substitute for authoritative web sources.

**Concrete failure case:** Adding the nrf52 example. The model searched local disk for nrf52 information instead of fetching current Nordic documentation, SDK changelog, or errata. The result was planning against stale or incomplete facts.

The desired outcome is a lower reactive trigger: whenever work references an external component, standard, or library not already characterized in the codebase, the researcher is invoked before planning commits to assumptions about that external thing.

## Scope

1. Tighten the `researcher` role description in AGENTS.md to express the lower reactive trigger clearly.
2. Add an optional `research` step (with an explicit trigger condition) to the four skill sequences most likely to involve external-component assumptions:
   - Product feature work
   - System definition / concept trade
   - Design cleanup
   - Bug work
3. Add one behavioral default in AGENTS.md's "Behavioral defaults" section that names the reactive trigger explicitly.

## Non-goals

- Do not make `research` a mandatory default step in every sequence.
- Do not change the researcher's stop condition — it still stops before option comparison or design.
- Do not change CLAUDE.md unless the AGENTS.md change alone is insufficient.
- Do not widen researcher scope to include option surfacing or recommendations.

## Constraints

- One small mutable surface: AGENTS.md only (unless evidence shows CLAUDE.md must also change).
- Changes must be backward-compatible: teams not using external components should see no difference.
- The trigger must be concrete enough that future agents can self-apply it without human prompting.

## Acceptance criteria (behavior terms)

1. Given a task that references a specific external MCU, SDK, vendor library, or standard not present in the codebase, the operating model directs the researcher to fetch current docs before planning starts.
2. Given a task that is entirely internal (refactoring existing code with no external dependencies), the researcher is not invoked.
3. The trigger wording in AGENTS.md is self-applying — a reader can determine within two sentences whether the researcher should fire for their task.
4. The four named skill sequences each contain an explicit optional `research` step with a one-line trigger condition.

## Assumptions / open questions

- Evaluation window: next 5 tasks that involve external components. Decision — keep / revise / revert — recorded in `docs/workflow-experiments/`.
- Researcher still returns raw facts only, no option comparison.

## TDD expectation

Non-productized workflow change. TDD is not applicable. Verification: human review of the edited AGENTS.md against the acceptance criteria above, plus a spot-check against the nrf52 failure case.

## Stakeholders

- Requester (firmware team lead): wants web research pulled in reactively on external-component work.
- Future model instances: the trigger must be self-applying.
