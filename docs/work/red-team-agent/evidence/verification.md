# Verification Record

## Storage

- Work ID: `red-team-agent`
- File path: `docs/work/red-team-agent/evidence/verification.md`
- Brief: `docs/work/red-team-agent/brief.md`
- Plan: `docs/work/red-team-agent/plan.md`
- Status: `docs/work/red-team-agent/status.md`

## Verifier

- Role: verifier
- Date: 2026-03-20

## Verification method

- Manual inspection of source files against AC-001 through AC-007 in `brief.md`
- Manual walkthrough of SC-001 through SC-003 by reading the new role, skill, template, and updated reviewer role
- Mechanical check with `python3 scripts/cli.py sync`
- Mechanical check with `python3 scripts/cli.py sync --check`

## Acceptance criteria results

- AC-001: pass — `.agents/agents/red-team.toml` exists with required fields, pre-implementation trigger, adversarial intent, return contract, and reviewer distinction
- AC-002: pass — `.agents/skills/plan-red-team/SKILL.md` exists with frontmatter, process, guardrails, done-when, output, and template reference
- AC-003: pass — `AGENTS.md` lists `red-team` under optional specialists and in the default flow after `planner` and before `developer` on medium/high-risk work
- AC-004: pass — `.agents/project/CLAUDE.md` includes matching when-to-use guidance for `red-team`
- AC-005: pass — `templates/red-team-findings-template.md` exists with storage, scope, findings, recommendation, and deferred concerns sections
- AC-006: pass — `python3 scripts/cli.py sync --check` exited 0 after source changes
- AC-007: pass — `CHANGELOG.md` contains an `Added` entry under `Unreleased` for the new role/skill/template set

## Scenario walkthrough

- SC-001: pass — the skill and template require structured findings with severity, referenced `plan.md` claim, and suggested resolution
- SC-002: pass — the skill and template constrain the recommendation to exactly one of approve, revise, or escalate
- SC-003: pass — `red-team.toml` and `reviewer.toml` explicitly distinguish pre-implementation plan challenge from post-implementation patch review

## Generated outputs

- `python3 scripts/cli.py sync` exited 0 and updated generated mirrors
- `python3 scripts/cli.py sync --check` exited 0 with no drift
- Expected generated artifacts include `.claude/agents/red-team.md`, `.github/agents/red-team.agent.md`, and `.codex/agents/red-team.toml`

## Residual risk

- No live invocation of the new `red-team` role was executed against a real work packet; usefulness was verified by static contract inspection, not by an end-to-end human workflow trial
- Verification did not include release packaging or a committed-history check

## Verdict

Verified. The implemented change satisfies the accepted scope and documented acceptance criteria.
