# Workflow Experiment

## Storage

- Experiment ID: `EXP-007-bias-copilot-toward-small-patches`
- File path: `docs/workflow-experiments/EXP-007-bias-copilot-toward-small-patches.md`
- Related work packets: `docs/work/copilot-small-patch-bias/`

## Problem / recurring friction

Copilot sometimes attempts a large patch in one jump, especially when a task spans several files or concerns. Those larger edits are more likely to fail to apply cleanly, produce avoidable churn, or leave the agent thrashing between broad retries.

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `.github/copilot-instructions.md`
  - `AGENTS.md`
  - `docs/copilot-vscode-playbook.md`
  - `docs/workflow-experiments/EXP-003-deepen-copilot-support.md`
  - `docs/workflow-experiments/EXP-005-copilot-role-model-selection.md`
  - direct requester feedback in this session: Copilot tends to try very large patches and fail
- What keeps going wrong:
  - Copilot can optimize for broad completion in one shot instead of stable staged progress
  - failed large edits increase retry churn
- Current cost:
  - lower edit success rate
  - less reviewable diffs
  - more time lost recovering from failed patch attempts

## Hypothesis

If the repo's Copilot-specific instructions explicitly tell Copilot to prefer narrow, staged patches and to reduce scope after a failed edit rather than escalating into an even broader patch, then Copilot will attempt smaller edits and recover more cleanly on non-trivial work.

## Small mutable surface

- Type: docs
- Exact artifact(s) to change:
  - `.github/copilot-instructions.md`
- Why this is the smallest plausible intervention:
  - the friction is specific to Copilot behavior
  - shared operating-model rules already say "smallest effective diff," so a Copilot-specific prompt tweak is lower-cost than changing the whole cross-tool contract
  - a new skill or role would be excessive for a guidance problem

## Proposed change

Add explicit Copilot guidance to:

- prefer narrow, staged patches over large all-at-once edits
- keep the active write surface small until the first slice is working
- shrink scope after a failed patch attempt instead of retrying with a broader edit

## Evaluation window

- Start condition:
  - the Copilot instruction update lands on the main branch
- End condition:
  - after the next `3` Copilot-led delivery tasks, or one month of use, whichever comes first
- Scope: `3` Copilot-led delivery tasks or one month

## Success signals

- Copilot-led tasks show smaller, more reviewable edit slices
- fewer failed patch attempts expand into larger retries
- users need fewer manual nudges to break work into smaller steps

## Failure signals / revert triggers

- Copilot becomes too timid and stalls on legitimate multi-file changes
- the new wording increases unnecessary micro-patches without improving success
- observed Copilot behavior does not change over the evaluation window

## SemVer / changelog impact

- `PATCH`: workflow clarification for existing Copilot guidance

## Rollout / migration notes

- no migration required
- this is a bias, not a ban on multi-file changes
- larger edits are still acceptable when they are part of one coherent, verified slice

## Result

- Decision: keep provisionally through the evaluation window
- Evidence observed:
  - initial landing only; no post-landing task evidence yet
- Follow-up:
  - review after the next `3` Copilot-led delivery tasks, or one month of use
