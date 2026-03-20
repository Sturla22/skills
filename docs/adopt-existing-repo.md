# Adopt Into An Existing Repo

This starter should support incremental adoption into an existing repository. Do not treat adoption as a greenfield rewrite.

## Goal

Introduce the smallest useful slice of the roles-and-skills workflow while preserving the existing repo's delivery constraints, team habits, and working automation.

## Start with preservation, not replacement

Before adding files, inventory the conventions that already matter:

- issue tracker IDs and branch naming
- commit message and PR title rules
- release process and versioning rules
- docs, ADR, and architecture note locations
- build, test, lint, and CI entry points
- any existing agent, prompt, or instruction files
- code ownership or review expectations

Record these in the work packet before proposing workflow changes.

## Recommended adoption levels

### Level 1: Instructions only

Use when the team wants a better prompting surface first.

- add `AGENTS.md`
- add `.github/copilot-instructions.md` if Copilot is in use
- add `.agents/project/CLAUDE.md` if Claude is in use
- keep the rest of the repo unchanged

### Level 2: Generated agents

Use when the team wants stable role entry points across tools.

- add `.agents/agents/*.toml`
- run `python3 scripts/cli.py sync`
- review generated files without forcing workflow changes on every task

### Level 3: Work packets for non-trivial tasks

Use when context drift or handoff loss is the main problem.

- adopt `docs/work/<work-id>/`
- use `brief.md`, `plan.md`, and `status.md` only for medium or higher complexity work
- leave small tasks on the repo's existing normal path

### Level 4: Skills and templates

Use when the team wants reusable execution patterns.

- add only the skills that solve recurring problems in the existing repo
- avoid importing every skill before there is evidence they help

### Level 5: Full workflow

Use when the team wants the repo to treat this model as the default operating shape.

## Suggested first pilot

Pick one real task, not a fake migration demo.

Good pilot candidates:

- a bug fix with multiple handoffs
- a docs update with release impact
- a risky refactor that needs verification discipline
- a tooling change that benefits from a brief and plan

Avoid starting with:

- the hardest architecture migration in the repo
- a release-critical task with no buffer
- an open-ended process redesign

## First-run path for existing repos

Use:

```bash
python3 scripts/cli.py doctor --tool codex --mode existing
python3 scripts/cli.py first-run --tool codex --mode existing
```

Replace `codex` with `claude` or `copilot` as needed.

## What not to replace immediately

- existing CI commands
- existing release gates
- existing docs or ADR locations that are already working
- existing PR templates or review rules
- existing branch naming or issue-linking rules

Map this workflow onto those constraints first. Only standardize further after a few successful pilots.

## Done when

- adopters can name the conventions being preserved
- one pilot task uses the workflow without disrupting delivery
- the repo has a clear recommended minimum adoption level
- the team can explain what changed and what intentionally did not
