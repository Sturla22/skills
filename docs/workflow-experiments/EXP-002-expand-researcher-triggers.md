# Workflow Experiment

## Storage

- Experiment ID: `EXP-002-expand-researcher-triggers`
- File path: `docs/workflow-experiments/EXP-002-expand-researcher-triggers.md`
- Related work packets: `docs/work/expand-researcher-triggers/`

## Problem / recurring friction

The `researcher` role trigger was set too high. The prior wording — "when a knowledge gap must be closed before planning is possible" — implied a hard planning blocker. In practice, work referencing external components (MCU families, vendor SDKs, libraries, or standards) proceeded with local-disk search as a substitute for authoritative web sources.

Concrete failure case: Adding the nrf52 example caused the model to search local disk for nrf52 information instead of fetching current Nordic documentation, SDK changelog, or errata. Planning committed to stale or incomplete assumptions.

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `docs/work/expand-researcher-triggers/brief.md`
  - `docs/work/expand-researcher-triggers/handoffs/001-product-owner-to-workflow-architect.md`
  - `AGENTS.md` (pre-change state)
- What keeps going wrong: researcher not triggered on external-component work; planning proceeds on local-disk assumptions without authoritative verification
- Current cost: planning errors, rework when authoritative sources later contradict local assumptions

## Hypothesis

Lowering the researcher trigger from "planning is blocked" to "work references an external component not already characterized in the codebase" will cause researcher to fire reactively on those tasks, reducing planning assumptions made without current authoritative sources.

## Small mutable surface

- Type: role description + behavioral default + skill sequence steps
- Exact artifact(s) to change: `AGENTS.md` only
- Why this is the smallest plausible intervention: the trigger is expressed in AGENTS.md role descriptions, the default role flow list, the behavioral defaults section, and the skill sequences. All four touch points are in one file. No new role, skill, or template is needed.

## Proposed change

Four targeted edits to `AGENTS.md`:

1. **Role description** (Optional specialists section): reworded `researcher` trigger from "when a knowledge gap must be closed before planning is possible" to "when work references an external component, standard, SDK, or library whose current state is not already characterized in the codebase; fires reactively on that reference, not only when planning is completely blocked."

2. **Default role flow** (item 12): reworded to match the lower reactive trigger.

3. **Behavioral defaults**: added one new default — "When work references a specific external component, standard, SDK, or library not already characterized in the codebase, invoke `researcher` to fetch current docs, errata, or ecosystem state before planning commits to assumptions about that external thing."

4. **Skill sequences**: added an optional `research` step with a one-line trigger condition to four sequences:
   - Product feature work (step 2, before planning)
   - Product bug work (step 2, before hypothesis-driven-debugging)
   - System definition / concept trade (step 3, before planning)
   - Platform migration (step 2, before planning) — chosen over Design cleanup because platform migration almost always references an external MCU family or vendor SDK not yet characterized in the repo; the trigger is self-evident and always applicable, whereas the Design cleanup trigger (pattern has external origin) is narrower and less common in firmware-team practice.

## Evaluation window

- Start condition: this experiment record is committed to main
- End condition: five tasks that reference an external component have been completed under the updated AGENTS.md
- Scope: next 5 work packets that involve an external component (MCU family, vendor SDK, library, or standard)

## Success signals

- Researcher is invoked on at least 4 of the 5 qualifying tasks before planning starts
- No qualifying task proceeds to planning with unverified external assumptions as a documented risk
- Tasks that are entirely internal (no external component references) do not trigger researcher
- Post-research planning notes cite authoritative sources rather than local-disk guesses

## Failure signals / revert triggers

- Researcher fires on purely internal tasks with no external component reference (over-broad trigger)
- Researcher is still skipped on tasks that explicitly reference an external component (trigger still too narrow or not self-applying)
- Research step creates coordination overhead without evidence of improved planning quality on any of the 5 tasks

## SemVer / changelog impact

- MINOR: backward-compatible addition of optional guidance; no existing workflow is broken; teams with no external component work see no change
- `CHANGELOG.md` should be updated under `Unreleased` / `Changed` when this experiment is kept

## Rollout / migration notes

- No migration required; the change adds optional steps and a lower trigger threshold
- Existing work packets in flight are unaffected; the change applies from the next task forward
- Model instances reading AGENTS.md will self-apply the new trigger without human prompting, which is the primary goal

## Result

- Decision: pending — evaluate after 5 qualifying tasks
- Evidence observed: (to be filled in after evaluation window closes)
- Follow-up: if kept, update `CHANGELOG.md` under `Unreleased`; if revised, narrow or broaden the trigger wording; if reverted, restore prior single-sentence researcher description
