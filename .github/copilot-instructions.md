# GitHub Copilot repository instructions

Read `AGENTS.md` first for the operating model.

## Copilot repo surfaces

- Use `AGENTS.md` for the shared roles-over-skills operating model.
- Use `.github/instructions/*.instructions.md` for path-specific guidance on tests, firmware, docs, and build-system files.
- Use `.github/agents/*.agent.md` when a custom specialist is a better fit than the default chat thread.

## Durable artifact rule

- For non-trivial tasks, create or update the canonical work packet under `docs/work/<work-id>/`.
- Use `brief.md` for shared understanding, `plan.md` for the execution plan, `status.md` for current owner and next step, and `evidence/` plus `handoffs/` for durable proof and transitions.
- Treat `~/.copilot/session-state/` and similar tool-local files as scratch only. They may help the current session, but they do not satisfy the repo's durable work-packet requirement.

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
- In stable docs and code comments, prefer current-state wording over historical narration. Put change history in `CHANGELOG.md`, ADR supersession, release notes, or work packets.
- Say clearly what was not verified on real hardware.

## Output expectations

When finishing a non-trivial task, include:
- the shared-understanding summary and current owner
- what changed
- why this approach was chosen
- what was verified
- what remains risky or unverified
