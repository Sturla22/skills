# Workflow Experiment

## Storage

- Experiment ID: `EXP-003-deepen-copilot-support`
- File path: `docs/workflow-experiments/EXP-003-deepen-copilot-support.md`
- Related work packets: none yet; evaluate on the next Copilot-led onboarding or delivery packets

## Problem / recurring friction

Copilot support in this repo was real but shallow. The repo already had `.github/instructions/*.instructions.md` files and enabled that path in `.vscode/settings.json`, but the Copilot-facing docs and `doctor --tool copilot` path did not treat that layer as a first-class, verified part of the support surface. That left a real capability under-explained and easy to miss during onboarding.

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `AGENTS.md`
  - `.github/copilot-instructions.md`
  - `.github/instructions/*.instructions.md`
  - `.vscode/settings.json`
  - `docs/copilot-vscode-playbook.md`
  - `docs/compatibility.md`
  - `README.md`
  - `tools/cli.py`
- What keeps going wrong:
  - the repo ships a Copilot path-specific instruction layer but under-explains it
  - Copilot diagnostics do not verify that layer
- Current cost:
  - weaker practical discoverability of repo-shaped guidance for Copilot than the repo actually provides
  - more onboarding guesswork for VS Code adopters

## Hypothesis

If the repo makes the existing `.github/instructions/` layer explicit in the Copilot docs and verifies it in `doctor --tool copilot`, then Copilot adopters will find and trust the path-aware guidance the repo already carries without introducing a new role, skill, or tool-specific prompt sprawl.

## Small mutable surface

- Type: docs + Copilot runtime support files
- Exact artifact(s) to change:
  - `.github/copilot-instructions.md`
  - `tools/cli.py`
  - `docs/copilot-vscode-playbook.md`
  - `docs/compatibility.md`
  - `README.md`
- Why this is the smallest plausible intervention:
  - a docs-only change would keep the support gap only partially fixed because diagnostics would still ignore the layer
  - a new skill or role would be overkill for a tool-surface gap
  - the change stays inside the existing Copilot repo-support layer

## Proposed change

Mention the existing path-specific instruction layer explicitly in the repo-wide Copilot instructions, and extend the Copilot playbook plus `doctor --tool copilot` so adopters can see and verify the layer.

## Evaluation window

- Start condition:
  - the new instruction files and docs are available on the main branch
- End condition:
  - after the next `3` Copilot-led onboarding or delivery packets, or one month of use, whichever comes first
- Scope: `3` Copilot-led packets or one month

## Success signals

- Copilot-led tasks reference the matching `.github/instructions/*.instructions.md` files when work is clearly in tests, docs, firmware, or build files
- `doctor --tool copilot` catches missing Copilot instruction-layer files in repos that drift
- onboarding notes stop treating `.github/instructions/` as an empty placeholder

## Failure signals / revert triggers

- the instruction files are too generic to influence Copilot behavior in practice
- the added files drift from the repo's real guidance and become stale duplication
- adopters report confusion about which layer to edit for cross-cutting vs path-specific guidance

## SemVer / changelog impact

- `MINOR`: additive Copilot support surfaces and onboarding guidance; no existing contract is broken

## Rollout / migration notes

- no migration required for existing adopters
- teams should edit the shipped `.github/instructions/*.instructions.md` files when they need Copilot-specific path guidance, and keep `AGENTS.md` plus `.github/copilot-instructions.md` for cross-cutting workflow guidance

## Result

- Decision: keep provisionally through the evaluation window
- Evidence observed:
  - initial landing only; no post-landing Copilot packet evidence yet
- Follow-up:
  - review after the next `3` Copilot-led onboarding or delivery packets, or one month of use
