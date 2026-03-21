# Workflow Experiment

## Storage

- Experiment ID: `EXP-001-bounded-autonomy-loop`
- File path: `docs/workflow-experiments/EXP-001-bounded-autonomy-loop.md`
- Related work packets: none yet; evaluate on the next suitable packets

## Problem / recurring friction

The repo has no reusable, bounded pattern for Ralph-style self-correcting execution loops.
That makes two bad outcomes likely:
- people improvise unbounded retry loops with weak stop conditions
- or the repo cannot reuse a useful autonomy pattern for narrow, auto-checkable slices

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `.agents/agents/product-owner.toml`
  - `.agents/agents/planner.toml`
  - `.agents/agents/developer.toml`
  - `.agents/project/CLAUDE.md`
  - `AGENTS.md`
  - `README.md`
  - `docs/templates/reusable-prompts.md`
- What keeps going wrong:
  - no durable repo-native pattern exists for fixed-budget autonomous iteration
- Current cost:
  - either missed reuse of a useful execution mode or unsafe free-form looping with weak escalation

## Hypothesis

If the repo adds a `bounded-autonomy-loop` skill plus a durable loop-log template, then `planner` and `developer` can use self-correcting execution safely for narrow slices with explicit done-when criteria, automated checks, and stop states.

## Small mutable surface

- Type: `skill`
- Exact artifact(s) to change:
  - `.agents/skills/bounded-autonomy-loop/SKILL.md`
  - `docs/templates/bounded-autonomy-loop-template.md`
  - the minimum role, prompt, and docs surfaces needed so the skill is discoverable and bounded correctly
- Why this is the smallest plausible intervention:
  - a prompt-only tweak would be too easy to miss
  - a new role would be overkill

## Proposed change

Add a reusable `bounded-autonomy-loop` skill, a durable loop-log template, and minimal planner/developer/docs guidance that treats this as an optional execution mode with explicit budget and escalation.

## Evaluation window

- Start condition:
  - the skill and template are available on the main branch
- End condition:
  - after the next `3` suitable work packets or one month of use, whichever comes first
- Scope: `3` suitable work packets or one month

## Success signals

- the skill is used only on narrow, auto-checkable slices
- loop logs are actually created under `docs/work/<work-id>/evidence/bounded-autonomy-loop.md`
- stop states are explicit instead of implied
- blocked or budget-exhausted cases escalate cleanly instead of looping indefinitely

## Failure signals / revert triggers

- the skill gets used on ambiguous design or unknown-cause debugging work
- loop logs are not maintained in practice
- budgets or stop states are routinely omitted
- the skill duplicates planning or TDD language without improving execution discipline

## SemVer / changelog impact

- `MINOR` if kept, because it adds a new optional skill and template

## Rollout / migration notes

- treat this as optional, not a new default
- route fit decisions through `planner` and `developer`
- revisit after the evaluation window and decide `keep`, `revise`, or `revert`

## Result

- Decision: keep provisionally through the evaluation window
- Evidence observed:
  - initial landing only; no internal work-packet usage yet
- Follow-up:
  - review after the next `3` suitable work packets or one month of use
