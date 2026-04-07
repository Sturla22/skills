# Work Plan

## Storage

- Work ID: `cli-first-work-packets`
- File path: `docs/work/cli-first-work-packets/plan.md`
- Source brief: `docs/work/cli-first-work-packets/brief.md`

## Problem statement

The repo already provides `tools/cli.py` commands for work-packet operations, but the workflow contract does not state strongly enough that supported CLI commands should be preferred over direct file creation when the CLI already models the operation.

## Stakeholders / system context

- Repo maintainers, agents, and reviewers rely on durable work packets under `docs/work/<work-id>/`
- `tools/cli.py` already supports `new-work`, `new-handoff`, `new-scenarios`, `check-work`, and `list-work`
- Copilot guidance and onboarding docs should align with the shared operating model

## Scope

- Clarify the shared workflow contract
- Clarify the Copilot-specific instruction surface
- Clarify onboarding guidance in `README.md`
- Record the change as a workflow experiment and in `CHANGELOG.md`

## Non-goals

- Add or change CLI features
- Expand the rule into a ban on direct content edits
- Redesign the broader workflow model

## Requirements / constraints / assumptions to keep visible

- Use the existing CLI capability as the supported path
- Keep the wording narrow: CLI-first for modeled operations, direct edits for substantive content
- Preserve the existing work-packet layout and role model

## Public contract / compatibility impact

- Additive workflow guidance only

## SemVer / changelog expectation

- `PATCH`

## Key behavior rules / scenarios

- New work packets should be scaffolded with `python3 tools/cli.py new-work <work-id>`
- New numbered handoffs should use `python3 tools/cli.py new-handoff <work-id> <from-role> <to-role>`
- Work-packet inspection should prefer `check-work` and `list-work`
- Agents may still edit scaffolded files directly to add task-specific content

## Trade studies / decision points

- Lowest-cost intervention chosen: docs and prompt clarification rather than new tooling
- Keep the rule framed as "supported CLI first" rather than "repo-owned CLI only"

## Preferred test strategy

- No TDD; this is a docs-only workflow clarification
- Verify by using the existing CLI to scaffold and check the current work packet
- Review the changed guidance surfaces directly

## Validation plan

- Observe the next `3` relevant tasks for CLI-first work-packet handling

## Walking skeleton

- Update the shared workflow docs
- Update the Copilot instruction surface
- Update the README onboarding guidance
- Add the workflow experiment and changelog entry
- Check the current work packet with `python3 tools/cli.py check-work cli-first-work-packets`

## Minimal configuration / iteration target

- One bounded workflow clarification slice with no tooling changes

## Exit criteria / milestone criteria

- All targeted docs state the CLI-first rule clearly
- The experiment record exists
- `CHANGELOG.md` records the clarification
- `check-work` passes for `cli-first-work-packets`

## Plan steps

1. Fill the canonical work packet with the problem, scope, and acceptance criteria.
2. Update the shared contract in `AGENTS.md` and `docs/operating-model.md`.
3. Update `.github/copilot-instructions.md` and `README.md` to mirror the rule.
4. Add `docs/workflow-experiments/EXP-008-cli-first-work-packets.md`.
5. Verify with `python3 tools/cli.py check-work cli-first-work-packets` and inspect the resulting diff.

## Parallel lanes

None.

## Ownership boundaries

- product-owner owns this docs-only workflow clarification end to end

## Blockers / dependencies

- None

## Verification gates

- `python3 tools/cli.py check-work cli-first-work-packets`
- Review changed files for wording consistency

## Risks / unknowns

- The guidance could be misread as forbidding direct content edits entirely if phrased too broadly

## Escalation triggers

- Escalate only if the existing CLI proves insufficient and the work turns into a tooling change
