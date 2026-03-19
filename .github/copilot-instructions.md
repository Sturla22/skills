# GitHub Copilot repository instructions

Read `AGENTS.md` first for the operating model.

## Repo-wide defaults

- Start non-trivial tasks by restating shared understanding, scope, non-goals, constraints, and acceptance criteria.
- Prefer BDD-style behavior scenarios for acceptance criteria and tests.
- Prefer the smallest effective diff.
- Separate planning, implementation, verification, and review.
- Prefer the test pyramid and simulation-first host checks before slower hardware-only checks when practical.
- Do not claim a fix without evidence.
- For risky refactors, add characterization tests first.
- For firmware code, keep hardware access behind explicit boundaries.
- Make units, timing assumptions, and failure behavior explicit.
- Update docs or ADR notes when design truth changes.
- Say clearly what was not verified on real hardware.

## Output expectations

When finishing a non-trivial task, include:
- the shared-understanding summary and current owner
- what changed
- why this approach was chosen
- what was verified
- what remains risky or unverified
