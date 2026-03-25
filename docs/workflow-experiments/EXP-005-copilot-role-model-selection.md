# Workflow Experiment

## Storage

- Experiment ID: `EXP-005-copilot-role-model-selection`
- File path: `docs/workflow-experiments/EXP-005-copilot-role-model-selection.md`
- Related work packets: evaluate on the next Copilot-led tasks that use custom agents

## Problem / recurring friction

The canonical role specs already express model preferences for Claude and Codex, but the GitHub Copilot generator ignored role-level model intent. That meant the repo could not make specific Copilot roles prefer a stronger model even when the role was clearly more planning- or critique-heavy than others.

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `.agents/agents/*.toml`
  - `.github/agents/*.agent.md`
  - `tools/cli.py`
  - `docs/copilot-vscode-playbook.md`
  - `docs/compatibility.md`
  - current GitHub Copilot custom-agent docs showing `model:` support in agent frontmatter
- What keeps going wrong:
  - Copilot roles lose role-level model intent during sync
  - model selection stays manual even for clearly reasoning-heavy custom agents
- Current cost:
  - weaker parity between Claude, Codex, and Copilot role generation
  - more manual IDE configuration when a role should consistently prefer a specific model

## Hypothesis

If canonical role specs can optionally declare `copilot_model`, and `tools/cli.py sync` emits that as `model:` in `.github/agents/*.agent.md`, then the repo can make selected Copilot roles prefer stronger models without forcing a model for every role or for the default chat thread.

## Small mutable surface

- Type: generator + canonical role specs + Copilot docs
- Exact artifact(s) to change:
  - `tools/cli.py`
  - selected `.agents/agents/*.toml`
  - `docs/copilot-vscode-playbook.md`
  - `docs/compatibility.md`
- Why this is the smallest plausible intervention:
  - a docs-only change would not survive sync
  - editing generated `.github/agents/*.agent.md` directly would drift immediately
  - a new role or skill would be unrelated to the real problem

## Proposed change

Add `copilot_model` support to canonical role specs, emit it into generated Copilot agent frontmatter during sync, set an explicit repo policy by role class, and document the limit that only explicit custom agents can be pinned this way.

## Evaluation window

- Start condition:
  - the generator and canonical role changes are available on the main branch
- End condition:
  - after the next `3` Copilot-led tasks that explicitly use custom agents, or one month of use, whichever comes first
- Scope: `3` Copilot custom-agent tasks or one month

## Success signals

- generated `.github/agents/*.agent.md` files retain `model:` after every sync
- selected Copilot roles show the expected model preference in IDE agent configuration
- users no longer need to hand-edit generated Copilot agent files to keep a role-level model preference

## Failure signals / revert triggers

- pinned model names prove incompatible with common Copilot plans or org policies
- synced agent files become less portable because model pinning is too aggressive
- users report that the selected roles should inherit defaults instead of pinning a model

## SemVer / changelog impact

- `MINOR`: additive generator and workflow capability; no existing role contract is broken

## Rollout / migration notes

- no migration required
- every canonical role now carries an explicit `copilot_model`
- if a team's plan or policy disallows a pinned model, they can change the canonical role spec and re-run sync

## Result

- Decision: keep provisionally through the evaluation window
- Evidence observed:
  - initial landing only; no post-landing task evidence yet
- Follow-up:
  - review after the next `3` Copilot custom-agent tasks, or one month of use
