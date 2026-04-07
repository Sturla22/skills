# Product Brief

## Storage

- Work ID: `cli-first-work-packets`
- File path: `docs/work/cli-first-work-packets/brief.md`

## Request summary

Strengthen the repo's workflow guidance so agents prefer supported CLI functions over direct file edits whenever the CLI already provides the operation, especially for work packets.

## Problem / desired outcome

The repo already ships `tools/cli.py` commands for work-packet scaffolding and inspection, but the workflow contract does not currently state strongly enough that supported CLI commands should be preferred over hand-creating files. The desired outcome is a clearer CLI-first rule, especially for work packets, handoffs, and scenario stubs.

## Why this matters

Manual creation of artifacts that the CLI already knows how to scaffold increases drift, inconsistency, and avoidable edit churn. Work packets are especially sensitive because they are durable coordination surfaces.

## Code drivers

- User scenarios — improve how agents and maintainers create and maintain work packets
- Risk — reduce avoidable workflow drift and malformed packet structures
- Design intent communication — make the repo's CLI-first expectation explicit in the contract

## Stakeholders / users

- Repo maintainers
- Agents operating under the repo contract
- Humans reading or reviewing durable work packets

## Stakeholder needs / system outcomes

- Work-packet scaffolding should be consistent and repeatable
- Agents should prefer supported CLI commands when available instead of improvising direct file creation
- The durable workflow should stay aligned with the CLI that already models it

## Design criteria / key parameters

- Prefer the smallest plausible intervention
- Strengthen guidance without banning normal content edits after scaffolding
- Keep the change focused on existing CLI capability rather than inventing new automation

## In scope

- Shared workflow guidance for preferring supported CLI operations
- Stronger work-packet-specific direction for `tools/cli.py` packet commands
- Copilot-facing prompt guidance that mirrors the shared contract

## Out of scope

- Adding new CLI subcommands
- Broad rewrite of the operating model
- Forbidding direct edits to task-specific file contents after scaffolding

## Constraints

- Use the existing `tools/cli.py` capability; this is a guidance change, not a tooling feature request
- Keep the change aligned with the current roles-over-skills model
- Treat this as a workflow-contract clarification with changelog impact
## Commit and PR title policy

- Existing issue tracker, commit, or PR conventions remain unchanged
- This slice does not change the Jira-ID policy

## Existing conventions to preserve

- Existing issue tracker, commit, or PR conventions: preserve the current logical-commit rule and current Jira-ID policy
- Existing release or branching process: no release-process change
- Existing docs, ADR, or architecture layout: preserve the existing work-packet layout under `docs/work/WORK-ID/`
- Existing build, test, and CI expectations: use existing CLI checks where available
- Existing agent, instruction, or automation files: preserve `tools/cli.py` as the repo-owned workflow entry point

## System context / external interfaces

- `tools/cli.py` already provides `new-work`, `new-handoff`, `new-scenarios`, `check-work`, and `list-work`
- Shared workflow contract lives in `AGENTS.md` and `docs/operating-model.md`
- Copilot-specific runtime guidance lives in `.github/copilot-instructions.md`
- README is the main onboarding surface for CLI-backed workflow expectations

## Acceptance criteria

- The shared workflow docs explicitly say to prefer supported CLI commands when they already provide the operation
- Work-packet guidance explicitly names the `tools/cli.py` commands to use for scaffolding and inspection
- Copilot-specific instructions mirror that rule
- The change is recorded as a bounded workflow experiment and in `CHANGELOG.md`
## Measures of effectiveness / performance

- On the next workflow tasks, agents scaffold work packets and related artifacts through the CLI rather than hand-creating them
- Reviewers need fewer reminders about using supported packet commands
## Behavior rules / examples (BDD)

- Given a supported CLI command that already models an operation, when an agent needs to perform that operation, then it should use the CLI instead of hand-creating the artifact
- Given a work packet that needs to be created or checked, when the repo provides packet commands, then the agent should use `tools/cli.py` for scaffolding and inspection and only edit the resulting files to add task-specific content

## Behavior scenarios (BDD)

### Scenario: scaffold a work packet

- Given a non-trivial task with a new work ID
- When the agent creates the durable work packet
- Then it uses `python3 tools/cli.py new-work WORK-ID` instead of hand-creating the packet files and directories

### Scenario: create a numbered handoff

- Given an existing work packet and a new owner transition
- When the agent creates the handoff artifact
- Then it uses `python3 tools/cli.py new-handoff WORK-ID FROM-ROLE TO-ROLE` instead of manually numbering the handoff file

### Scenario: fill scaffolded content

- Given a packet or handoff file created by the CLI
- When the agent needs to capture task-specific truth
- Then it edits the scaffolded file content directly rather than expecting the CLI to author the substantive task details

## Derived requirements / traceability notes

- The CLI-first rule should be explicit enough to change behavior but narrow enough not to ban ordinary content edits
## Public contract / compatibility impact

- Additive workflow guidance only; no existing command or path is removed
## Delivery class

- Non-productized workflow improvement
## TDD expectation

- Not applicable; verification comes from reading the affected surfaces and using the existing CLI to scaffold and check the work packet
## Validation intent / evidence

- No separate stakeholder-fit validation needed beyond observing whether future tasks follow the stronger CLI-first guidance
## SemVer / changelog expectation

- `PATCH`: clarification of an existing workflow convention around existing CLI capabilities
## Assumptions

- The existing CLI commands are the right stable entry points for packet operations
- The main problem is guidance strength, not missing functionality
## Open questions

- Whether similar CLI-first wording should later be expanded beyond work-packet operations to other repo-owned tooling surfaces
## Recommended next owner(s)

- product-owner for the current docs-only workflow clarification
## Parallelization notes

- No parallel write lanes needed
## Delegation notes

- No specialist handoff needed; the change is a bounded docs-and-prompt clarification
