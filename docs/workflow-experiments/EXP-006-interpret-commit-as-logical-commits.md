# Workflow Experiment

## Storage

- Experiment ID: `EXP-006-interpret-commit-as-logical-commits`
- File path: `docs/workflow-experiments/EXP-006-interpret-commit-as-logical-commits.md`
- Related work packets: `docs/work/commit-means-logical-commits/`

## Problem / recurring friction

The repo already prefers one logical change per commit, but a plain user instruction such as "commit" still leaves room for an agent to interpret that as "make one commit now" instead of "make the history logically reviewable."

That ambiguity shows up at the moment of handoff to git:
- the user has authorized committing
- the operating model prefers logical commits
- the model still has to guess whether multiple logical commits are allowed

## Evidence baseline

- Work packets, prompts, handoffs, or artifacts reviewed:
  - `AGENTS.md`
  - `docs/operating-model.md`
  - `.agents/project/CLAUDE.md`
  - `.github/copilot-instructions.md`
  - direct requester feedback in this session: when they say "commit," they want logical commits
- What keeps going wrong:
  - the permission to commit is clearer than the expected commit granularity
  - agents can optimize for compliance with "commit" instead of reviewable history
- Current cost:
  - reduced commit readability
  - mixed logical changes in one commit when the user did not actually ask for that tradeoff

## Hypothesis

If the operating model says explicitly that a bare request to "commit" authorizes one or more logical commits, unless the requester asks for a single combined commit, then agents will preserve atomic history more consistently without needing follow-up clarification.

## Small mutable surface

- Type: docs
- Exact artifact(s) to change:
  - `AGENTS.md`
  - `docs/operating-model.md`
- Why this is the smallest plausible intervention:
  - the problem is an interpretation gap in the shared operating model
  - a tool change or new skill would be heavier than necessary
  - repo-wide instruction files already point back to `AGENTS.md` for the operating model

## Proposed change

Add explicit wording that:
- a bare user request to "commit" means create one or more logical commits
- a single umbrella commit should be used only when the requester asks for that tradeoff explicitly

## Evaluation window

- Start condition:
  - the operating-model wording lands on the main branch
- End condition:
  - after the next `3` tasks where the requester asks to commit, or one month of use, whichever comes first
- Scope: `3` commit-request tasks or one month

## Success signals

- commit-request tasks produce logical commits without extra clarification
- fewer sessions need follow-up prompts about whether one commit or several are expected
- commit history better matches the repo's existing atomic-commit policy

## Failure signals / revert triggers

- agents over-split tiny changes into noisy micro-commits
- the wording is misread as permission to rewrite already shared history
- users frequently expected one combined commit and find the new behavior surprising

## SemVer / changelog impact

- `PATCH`: workflow clarification consistent with the existing logical-commit policy

## Rollout / migration notes

- no migration required
- users who want one combined commit should say so explicitly

## Result

- Decision: keep provisionally through the evaluation window
- Evidence observed:
  - initial landing only; no post-landing task evidence yet
- Follow-up:
  - review after the next `3` commit-request tasks, or one month of use
