# Workflow Experiment

## Storage

- Experiment ID: `EXP-008-cli-first-work-packets`
- File path: `docs/workflow-experiments/EXP-008-cli-first-work-packets.md`
- Related work packets: `docs/work/cli-first-work-packets/`

## Problem / recurring friction

The repo already has CLI support for work-packet scaffolding and inspection, but agents can still hand-create packet files, handoffs, or scenario stubs as if the CLI did not exist. That increases avoidable drift and misses the supported workflow surface that was built to keep these artifacts consistent.

This is most visible around work packets:

- `new-work` can scaffold the packet layout
- `new-handoff` can generate the next numbered handoff stub
- `new-scenarios` can create scenario files
- `check-work` and `list-work` can inspect packet state

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `AGENTS.md`
  - `docs/operating-model.md`
  - `.github/copilot-instructions.md`
  - `README.md`
  - `tools/cli.py`
  - `docs/workflow-experiments/EXP-004-force-work-packets-over-session-state.md`
  - direct requester feedback in this session: there should be a strong direction to use CLI functions rather than editing files directly, especially for work packages
- What keeps going wrong:
  - existing docs say the work packet is canonical, but they do not say strongly enough that supported CLI-backed packet operations should use the CLI first
  - agents can still improvise packet scaffolding manually
- Current cost:
  - inconsistent packet creation habits
  - avoidable manual work on numbered or boilerplate artifacts
  - weaker alignment between the documented workflow and the supported tooling

## Hypothesis

If the shared operating-model docs, the Copilot-specific instruction surface, and the onboarding README explicitly say to prefer supported CLI commands whenever the CLI already models the operation, especially for work packets, then agents will use `tools/cli.py` for scaffolding and inspection more consistently and reviewers will need fewer reminders.

## Small mutable surface

- Type: docs
- Exact artifact(s) to change:
  - `AGENTS.md`
  - `docs/operating-model.md`
  - `.github/copilot-instructions.md`
  - `README.md`
- Why this is the smallest plausible intervention:
  - `tools/cli.py` already provides the needed capability
  - the problem is a workflow-contract and prompt gap, not missing automation
  - changing docs and prompts is lower-cost than adding new tooling or roles

## Proposed change

Add an explicit CLI-first rule:

- when a supported CLI already provides the operation, use that CLI rather than hand-creating or hand-auditing the artifact
- for work packets, call out `new-work`, `new-handoff`, `new-scenarios`, `check-work`, and `list-work`
- preserve direct edits for filling in task-specific content after scaffolding

## Evaluation window

- Start condition:
  - the docs update lands on the main branch
- End condition:
  - after the next `3` workflow-change or Copilot-led non-trivial tasks, or one month of use, whichever comes first
- Scope: `3` relevant tasks or one month

## Success signals

- new work packets are scaffolded with `tools/cli.py new-work`
- numbered handoff stubs and scenario stubs are created with the CLI when applicable
- reviewers need fewer reminders to use supported packet commands

## Failure signals / revert triggers

- the wording causes confusion that direct content edits are forbidden entirely
- observed behavior does not change over the evaluation window
- the change adds prompt/docs noise without affecting work-packet handling

## SemVer / changelog impact

- `PATCH`: clarification of existing workflow guidance around existing CLI capabilities

## Rollout / migration notes

- no migration required
- this is a preference for CLI-backed operations, not a ban on editing file contents
- the repo still expects humans and agents to fill in scaffolded files directly with task-specific truth

## Result

- Decision: keep provisionally through the evaluation window
- Evidence observed:
  - initial landing only; no post-landing task evidence yet
- Follow-up:
  - review after the next `3` workflow-change or Copilot-led non-trivial tasks, or one month of use
