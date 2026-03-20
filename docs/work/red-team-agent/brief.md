# Product Brief

## Storage

- Work ID: `red-team-agent`
- File path: `docs/work/red-team-agent/brief.md`

## Request summary

Add a `red-team` agent that adversarially challenges `plan.md` on medium
and high-risk work, returning structured findings to `product-owner`
before implementation starts.

## Problem / desired outcome

Plans produced by `planner` are currently reviewed only by `product-owner`
informally. There is no dedicated adversarial pass that tries to break the
plan — exposing optimistic assumptions, underspecified acceptance criteria,
missing risks, hidden dependencies, and scope ambiguities — before a
developer starts work. This increases the likelihood that problems surface
during implementation rather than during planning.

Desired outcome: a `red-team` role that fires after `planner` writes
`plan.md` on medium/high-risk work, produces a structured findings document,
and returns a clear recommendation to `product-owner` (approve / revise /
escalate) before any code is written.

## Why this matters

The cost of finding a plan flaw before implementation is far lower than
finding it mid-development. An adversarial pass also prevents optimism bias
— the planner is naturally invested in the plan it wrote; `red-team`'s job
is to attack it without that investment.

## Stakeholders / users

- **product-owner** — receives `red-team` findings and acts on them
- **planner** — primary target of review; findings may trigger a plan revision
- **developer** — benefits from a cleaner plan before implementation starts
- **repo adopters** — inherit the role and can invoke it on their own work

## Stakeholder needs / system outcomes

1. Plans on medium/high-risk work are challenged before implementation starts.
2. Findings are structured, actionable, and distinct from post-implementation review.
3. `product-owner` gets a clear recommendation (approve / revise / escalate), not just a list of concerns.
4. The role is invocable by any orchestrator that knows what risk level the work carries.

## Design criteria / key parameters

- Role name: `red-team`
- Fires after `planner` writes `plan.md`; before `developer` starts
- Scope: medium and high-risk work (risk level decided by `product-owner` or `planner`)
- Output: a structured findings document — not an inline edit of `plan.md`
- Returns findings to `product-owner`, not directly to requester
- Must be distinguishable from `reviewer` (which fires post-implementation)

## In scope

- New agent role: `.agents/agents/red-team.toml`
- New skill: `.agents/skills/plan-red-team/SKILL.md` — adversarial plan review process
- `AGENTS.md` update: add `red-team` to optional specialists, default flow, and where it sits
- `.agents/project/CLAUDE.md` update: when-to-use guidance
- A findings document template under `templates/`
- `scripts/cli.py sync` run to propagate generated files
- `CHANGELOG.md` MINOR entry

## Out of scope

- Automated triggering (CI, hooks) — manual invocation only in v1
- Scoring or quantitative risk ranking
- Modifying `plan.md` directly — findings go in a separate document
- Post-implementation review (that stays with `reviewer`)
- Security red-teaming of code or firmware

## Constraints

- Agent TOML must follow the existing stub pattern; stdlib-only, no new dependencies
- Skill must follow the `SKILL.md` frontmatter convention
- Role name must be a single lowercase hyphenated word to match existing naming
- Findings template must be human-readable without tooling
- No TDD required (non-productized tooling)

## System context / external interfaces

- Reads: `plan.md`, `brief.md`, `status.md` from the work packet
- Writes: a findings document, conventionally stored under
  `docs/work/<work-id>/evidence/red-team-findings.md`
- Returns findings to `product-owner` via the standard handoff pattern
- No hardware, no pip dependencies, no build system

## Acceptance criteria

- AC-001: `.agents/agents/red-team.toml` exists with correct fields and a clear role description covering adversarial intent, when to invoke, and return contract.
- AC-002: `.agents/skills/plan-red-team/SKILL.md` exists with frontmatter, process steps, findings template, and guardrails.
- AC-003: `AGENTS.md` lists `red-team` under optional specialists and in the default flow at the correct position (after `planner`, before `developer`, on medium/high-risk work).
- AC-004: `.agents/project/CLAUDE.md` includes a `red-team` when-to-use bullet consistent with AC-003.
- AC-005: `templates/red-team-findings-template.md` exists with all required sections.
- AC-006: `scripts/cli.py sync --check` exits 0 after all changes.
- AC-007: `CHANGELOG.md` has a new `Added` entry under `Unreleased`.

## Measures of effectiveness / performance

- `product-owner` can invoke `red-team` after planner with no ambiguity about what it should produce
- Findings doc is distinct from `reviewer` output and clearly scoped to plan-time concerns

## Behavior rules / examples (BDD)

- Given a `plan.md` exists for a medium-risk work item, when `red-team` reviews it, then it produces a findings document naming each challenged assumption, risk, or gap with a severity and a suggested resolution.
- Given findings exist, when `red-team` returns to `product-owner`, then it includes one of: "approve as-is", "revise plan before proceeding", or "escalate — plan has unresolvable gaps".

## Behavior scenarios (BDD)

Will be captured in `docs/work/red-team-agent/scenarios.md` as part of Step 0 in the plan.

## Derived requirements / traceability notes

- The `red-team` role must not overlap `reviewer`'s mandate — separation must be explicit in both role descriptions.
- The findings doc must reference the specific `plan.md` section or claim it challenges, not just assert a vague concern.

## Public contract / compatibility impact

New optional specialist role. No existing role renames or contract changes.
MINOR version impact — backward-compatible addition.

## Delivery class

Non-productized tool (agent/skill/template additions). TDD not required.
Verification: human review of the produced files against acceptance criteria.

## TDD expectation

Not required. Verification is manual inspection of each AC against the
produced files plus `scripts/cli.py sync --check`.

## Validation intent / evidence

Not a stakeholder-fit question — adopters will know immediately whether
the role is useful by invoking it. No separate validation evidence needed.

## SemVer / changelog expectation

**MINOR** — new optional role, backward-compatible. `CHANGELOG.md` gets
a new `Added` entry under `Unreleased`.

## Assumptions

- "Medium/high risk" is a judgment call by `product-owner` or `planner`;
  no mechanical risk-scoring is needed in v1.
- The findings template is sufficient for v1; scoring or severity levels
  beyond High/Medium/Low are out of scope.
- `red-team` will not modify `plan.md` inline; all feedback goes in a
  separate findings document.

## Open questions

None — all decisions locked above.

## Recommended next owner(s)

`planner` — to sequence the steps, confirm no open questions remain,
and write `plan.md`.

## Parallelization notes

Single serial lane. Work is small enough that parallelism adds overhead.

## Delegation notes

Planner should return `plan.md` to product-owner for approval before
developer starts. Developer implements all deliverables in one lane and
syncs at the end.
