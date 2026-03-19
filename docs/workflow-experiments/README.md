# Workflow Experiments

Store bounded process-improvement experiments under this folder.

## Goal

Treat workflow changes like small, testable experiments instead of permanent philosophy changes made in one shot.

## Convention

- Store one Markdown file per experiment under `docs/workflow-experiments/`.
- Use a stable, sortable name such as:
  - `EXP-001-handoff-delta-discipline.md`
  - `EXP-002-planner-exit-criteria.md`
- Prefer one small mutable surface per experiment:
  - one prompt
  - one template
  - one skill
  - one role
- Define an explicit evaluation window, for example:
  - the next `3` work packets
  - one milestone
  - one week of use
- End every experiment with a decision:
  - `keep`
  - `revise`
  - `revert`

## What belongs here

- process changes proposed by `workflow-architect`
- lightweight experiments for prompts, templates, skills, or roles
- evidence and decisions about whether a workflow change helped

## What does not belong here

- normal product work packets under `docs/work/`
- architecture decision records
- free-form retrospectives with no bounded experiment or decision

## Template

- `templates/workflow-experiment-template.md` -> `docs/workflow-experiments/<experiment-id>.md`
