# GitHub Copilot repository instructions

Read `AGENTS.md` first for the operating model.

## Repo-wide defaults

- Prefer the smallest effective diff.
- Separate planning, implementation, verification, and review.
- Do not claim a fix without evidence.
- For risky refactors, add characterization tests first.
- For firmware code, keep hardware access behind explicit boundaries.
- Make units, timing assumptions, and failure behavior explicit.
- Update docs or ADR notes when design truth changes.
- Say clearly what was not verified on real hardware.

## Output expectations

When finishing a non-trivial task, include:
- what changed
- why this approach was chosen
- what was verified
- what remains risky or unverified
