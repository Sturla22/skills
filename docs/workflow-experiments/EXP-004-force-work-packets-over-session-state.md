# Workflow Experiment

## Storage

- Experiment ID: `EXP-004-force-work-packets-over-session-state`
- File path: `docs/workflow-experiments/EXP-004-force-work-packets-over-session-state.md`
- Related work packets: evaluate on the next Copilot-led non-trivial tasks

## Problem / recurring friction

Copilot can keep tool-local planning artifacts under `~/.copilot/session-state/`. In practice, those files can compete with the repo's operating model and make it look as though the durable planning requirement has been satisfied even when `docs/work/<work-id>/brief.md`, `plan.md`, and `status.md` were never created or updated.

That creates a workflow split:
- the repo says the work packet is canonical
- Copilot can still appear to "have a plan" without touching the work packet

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `AGENTS.md`
  - `docs/operating-model.md`
  - `.agents/agents/product-owner.toml`
  - `.agents/agents/planner.toml`
  - `.github/copilot-instructions.md`
  - `docs/copilot-vscode-playbook.md`
  - `tools/cli.py`
  - observed Copilot behavior in this repo using `~/.copilot/session-state/plan.md`
- What keeps going wrong:
  - session-local artifacts can substitute for durable work-packet updates in practice
  - Copilot onboarding prompts do not explicitly reject that substitution
- Current cost:
  - durable task truth can stay outside the repo
  - handoffs and later sessions lose context that should have lived in `docs/work/<work-id>/`

## Hypothesis

If the canonical `product-owner` and `planner` roles, the shared operating-model docs, and the Copilot-specific instruction and onboarding prompts all say explicitly that `~/.copilot/session-state/` is scratch only and not a substitute for the work packet, then Copilot-led non-trivial work will create and maintain `docs/work/<work-id>/` artifacts more consistently.

## Small mutable surface

- Type: role prompts + docs + Copilot onboarding prompts
- Exact artifact(s) to change:
  - `.agents/agents/product-owner.toml`
  - `.agents/agents/planner.toml`
  - `AGENTS.md`
  - `docs/operating-model.md`
  - `.github/copilot-instructions.md`
  - `docs/copilot-vscode-playbook.md`
  - `tools/cli.py`
- Why this is the smallest plausible intervention:
  - a Copilot playbook note alone is too weak
  - a new role or skill would be overkill
  - the problem is a prompt and operating-model contract gap, not a missing capability

## Proposed change

Make the scratch-vs-canonical distinction explicit across the operating model and Copilot-facing surfaces:

- canonical work packet under `docs/work/<work-id>/` is the durable truth
- `~/.copilot/session-state/` may exist as runtime scratch, but it does not satisfy the repo's brief / plan / status requirement

## Evaluation window

- Start condition:
  - the prompt and docs changes are available on the main branch
- End condition:
  - after the next `3` Copilot-led non-trivial tasks, or one month of use, whichever comes first
- Scope: `3` Copilot-led non-trivial tasks or one month

## Success signals

- Copilot-led non-trivial tasks create or update `docs/work/<work-id>/brief.md`, `plan.md`, and `status.md` when appropriate
- reviewers no longer need to remind Copilot that session-state files are not canonical
- later sessions can recover context from the work packet instead of depending on prior chat state

## Failure signals / revert triggers

- Copilot still routinely keeps the only plan in `~/.copilot/session-state/`
- the wording causes confusion about whether session-local scratch is forbidden entirely instead of merely non-canonical
- the extra prompt text adds overhead without changing observed behavior on the next `3` tasks

## SemVer / changelog impact

- `MINOR`: additive workflow guidance and stronger Copilot onboarding prompts; no existing contract is broken

## Rollout / migration notes

- no migration required
- this does not require deleting or disabling `~/.copilot/session-state/`
- teams should treat any tool-local scratch as ephemeral and mirror durable truth into `docs/work/<work-id>/`

## Result

- Decision: keep provisionally through the evaluation window
- Evidence observed:
  - initial landing only; no post-landing task evidence yet
- Follow-up:
  - review after the next `3` Copilot-led non-trivial tasks, or one month of use
