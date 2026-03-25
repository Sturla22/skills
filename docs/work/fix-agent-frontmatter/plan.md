# Work Plan

## Storage

- Work ID: `fix-agent-frontmatter`
- File path: `docs/work/fix-agent-frontmatter/plan.md`
- Source brief: `docs/work/fix-agent-frontmatter/brief.md`

## Problem statement

Custom agents fail to load because their frontmatter `description` fields are invalid YAML plain scalars.

## Stakeholders / system context

- Maintainers and contributors rely on `.github/agents/` as part of the repo workflow contract.

## Scope

- Fix malformed frontmatter in custom agent files.
- Verify all agent frontmatter parses successfully.

## Non-goals

- Changing agent behavior, wording, or role boundaries beyond YAML quoting.

## Requirements / constraints / assumptions to keep visible

- Preserve current descriptions exactly except for YAML-safe quoting.
- Avoid unrelated edits.

## Public contract / compatibility impact

- Behavior-preserving repair only.

## SemVer / changelog expectation

- No release-facing doc change expected.

## Key behavior rules / scenarios

- YAML parsing must succeed for every `.agent.md` frontmatter block.

## Preferred test strategy

- Focused parser validation of each agent file after the edit.

## Validation plan

- Not applicable beyond parser verification.

## Walking skeleton

- Patch all `description` fields to quoted scalars.

## Exit criteria / milestone criteria

- All agent files parse successfully.
- Git diff is limited to frontmatter and minimal work-packet/session-plan files.

## Plan steps

1. Confirm the malformed-frontmatter pattern across agent files.
2. Quote every affected `description` value.
3. Run parser-based verification across `.github/agents/*.agent.md`.
4. Summarize residual risk if any loader issue remains.

## Parallel lanes

- None

## Ownership boundaries

- Single-lane implementation and verification in the main thread.

## Blockers / dependencies

- None identified.

## Verification gates

- Local parse check passes for every agent file.

## Risks / unknowns

- Another loader rule could exist beyond YAML parsing, but the reported errors point to one root cause.

## Escalation triggers

- If parser validation still fails after quoting, inspect additional frontmatter fields or loader-specific constraints.
