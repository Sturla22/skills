# Plan: red-team-agent

## Storage

- Work ID: `red-team-agent`
- File path: `docs/work/red-team-agent/plan.md`
- Brief: `docs/work/red-team-agent/brief.md`
- Status: `docs/work/red-team-agent/status.md`

---

## Problem statement

Plans produced by `planner` are currently reviewed only by `product-owner` informally.
There is no adversarial pass that tries to break the plan — exposing optimistic assumptions,
underspecified acceptance criteria, hidden dependencies, and scope ambiguities — before a
developer starts work. When the work is done, the following must be true:

- A `red-team` optional specialist role exists in the repo with a TOML, a skill, and a
  findings template.
- `AGENTS.md` and `.agents/project/CLAUDE.md` document when to invoke it.
- All generated files are in sync (`scripts/cli.py sync --check` exits 0).
- `CHANGELOG.md` records the addition under `Unreleased`.

---

## Delivery class and TDD expectation

**Non-productized tool.** TDD is not required.

Verification replacement: manual inspection of each produced file against the seven
acceptance criteria in `brief.md`, plus `scripts/cli.py sync --check` as a mechanical
gate. This is documented explicitly as the verification strategy for this work.

---

## Stakeholders / system context

| Stakeholder | Interest |
|---|---|
| product-owner | invokes red-team after planner; acts on findings |
| planner | primary target of review; may revise plan.md in response |
| developer | receives a cleaner plan before implementation starts |
| repo adopters | inherit the role; invoke it on their own work |

**System context:** The repo contract is a set of role names, skill names, template names,
and canonical file paths under `.agents/`. Adding an optional specialist extends this
contract backward-compatibly.

**External interfaces:** No hardware. No pip dependencies. No build system changes.
The only machine-checkable gate is `scripts/cli.py sync --check`.

**Lifecycle:** All deliverables land in a single serial lane on `main`.

---

## Scope

- New file: `.agents/agents/red-team.toml`
- New file: `.agents/skills/plan-red-team/SKILL.md`
- New file: `templates/red-team-findings-template.md`
- Updated file: `AGENTS.md` (optional specialists section, default flow)
- Updated file: `.agents/project/CLAUDE.md` (when-to-use bullet)
- Run: `scripts/cli.py sync` (propagates generated files)
- Updated file: `CHANGELOG.md` (new `Added` entry under `Unreleased`)

## Non-goals

- Automated triggering (CI, hooks) — manual invocation only in v1
- Scoring or quantitative risk ranking
- Modifying `plan.md` directly — findings go in a separate document
- Post-implementation review (stays with `reviewer`)
- Security red-teaming of code or firmware

---

## Requirements / constraints / assumptions to keep visible

**Stakeholder needs:**

- SN-1: Plans on medium/high-risk work are challenged before implementation starts.
- SN-2: Findings are structured, actionable, and distinct from post-implementation review.
- SN-3: `product-owner` receives a clear approve / revise / escalate recommendation.
- SN-4: The role is invocable by any orchestrator that knows the work's risk level.

**Explicit requirements (from brief ACs):**

- R-001 (AC-001): `.agents/agents/red-team.toml` exists with correct fields, adversarial intent, when-to-invoke, and return contract.
- R-002 (AC-002): `.agents/skills/plan-red-team/SKILL.md` exists with frontmatter, process steps, findings-template reference, and guardrails.
- R-003 (AC-003): `AGENTS.md` lists `red-team` under optional specialists and in the default flow after `planner`, before `developer`, conditioned on medium/high-risk work.
- R-004 (AC-004): `.agents/project/CLAUDE.md` has a `red-team` when-to-use bullet consistent with R-003.
- R-005 (AC-005): `templates/red-team-findings-template.md` exists with all required sections.
- R-006 (AC-006): `scripts/cli.py sync --check` exits 0 after all changes.
- R-007 (AC-007): `CHANGELOG.md` has a new `Added` entry under `Unreleased`.

**Derived requirements:**

- DR-1 (from SN-2, brief §Derived): `red-team` and `reviewer` separation must be explicit in both role descriptions. Each must state the other's distinct scope.
- DR-2 (from SN-2, brief §Derived): Findings must reference the specific `plan.md` section or claim challenged, not assert a vague concern.
- DR-3 (from brief §Constraints): Agent TOML must follow the existing stub pattern; no new dependencies.
- DR-4 (from brief §Constraints): Role name is `red-team` — single lowercase hyphenated word.
- DR-5 (from brief §Constraints): Findings template must be human-readable without tooling.

**Constraints:**

- Single serial lane; parallelism adds coordination overhead with no benefit for this scope.
- SKILL.md must use `---` YAML frontmatter with at minimum `name:`, `description:`, and `allowed-tools:` fields, matching the convention in `.agents/skills/requirements-and-traceability/SKILL.md`.
- TOML fields must match the pattern of existing agent TOMLs: `name`, `description`, `tools`, `skills`, `claude_max_turns`, `codex_model_reasoning_effort`, `codex_sandbox_mode`, `codex_nickname_candidates`, `body`.

**Assumptions (from brief, preserved across handoffs):**

- "Medium/high risk" is a judgment call by `product-owner` or `planner`; no mechanical scoring in v1.
- Severity levels High/Medium/Low are sufficient; no finer-grained scoring needed.
- `red-team` will never modify `plan.md` inline; all feedback goes in a separate findings document.

---

## Public contract / compatibility impact

New optional specialist role. No existing role renames or contract changes.
MINOR version impact — backward-compatible addition.

## SemVer / changelog expectation

**MINOR.** New optional role, skill, and template. `CHANGELOG.md` gets a new `Added`
entry under `Unreleased`. No version bump in this plan step — version is bumped at release.

---

## Key behavior rules / scenarios

**SC-001 — Adversarial plan review produces structured findings**
Given a `plan.md` exists for a medium-risk work item,
when `red-team` reviews it using the `plan-red-team` skill,
then it produces a findings document that names each challenged assumption, risk, or gap
with a severity (High / Medium / Low) and a suggested resolution,
and each finding references the specific `plan.md` section or claim it challenges.

**SC-002 — Findings include a clear recommendation**
Given findings have been produced,
when `red-team` returns them to `product-owner`,
then the findings document includes exactly one of:
"approve as-is", "revise plan before proceeding", or "escalate — plan has unresolvable gaps."

**SC-003 — red-team is distinguishable from reviewer**
Given the `red-team.toml` and `reviewer.toml` both exist,
when a user reads them side by side,
then each document makes the other's distinct scope explicit:
`red-team` fires pre-implementation on `plan.md`; `reviewer` fires post-implementation on patches.

---

## Trade studies / decision points

None. All design decisions are locked in the brief. No credible competing options remain.

---

## Preferred test strategy

Non-productized tooling — no automated test pyramid applies. Verification is:

1. Manual AC inspection (verification gate A) — all five file-level ACs checked before sync.
2. `scripts/cli.py sync --check` (mechanical gate, AC-006).
3. CHANGELOG inspection (AC-007).
4. BDD scenario walkthrough (SC-001 through SC-003) by reading produced files side by side.

---

## Validation plan

Not a meaningful concern for this slice. Adopters will know immediately whether the role
is useful by invoking it. No separate validation evidence is required.

---

## Walking skeleton

The thinnest viable slice is: `red-team.toml` (defines the role) + `AGENTS.md` update
(makes it reachable) + sync pass (confirms the repo is coherent). Once those three exist,
the role is invocable even if the skill and template are stubs.

In practice, for this small scope, the full deliverable is small enough that the walking
skeleton and the final deliverable are the same work.

---

## Minimal configuration / iteration target

All seven ACs met in a single pass. No phased delivery needed.

## Exit criteria / milestone criteria

- All seven ACs pass manual inspection.
- `scripts/cli.py sync --check` exits 0.
- All three BDD scenarios are satisfied by inspection.
- `CHANGELOG.md` has the `Added` entry.
- No files outside declared write surfaces were modified.
- `plan.md` returned to product-owner and approved.

---

## Plan steps

### Step 1 — Author `.agents/agents/red-team.toml`

**Owner:** developer
**Depends on:** nothing (first step)
**Write surface:** `.agents/agents/red-team.toml` (new file)

**Acceptance criteria (maps to AC-001, R-001, DR-1, DR-3, DR-4):**

- File exists at `.agents/agents/red-team.toml`.
- `name = "red-team"` (single lowercase hyphenated word).
- `description` is a one-line summary that makes adversarial intent and pre-implementation scope clear.
- `tools` list is present; follows the existing agent pattern (at minimum `Read`, `Grep`, `Glob`, `Edit`).
- `skills` list references `plan-red-team` plus any supporting skills (e.g. `codebase-exploration`).
- `claude_max_turns`, `codex_model_reasoning_effort`, `codex_sandbox_mode`, `codex_nickname_candidates` are all present and plausible.
- `body` covers: adversarial intent, when to invoke (after `planner` writes `plan.md`, before `developer` starts, medium/high-risk work only), return contract (approve / revise / escalate to `product-owner`), and an explicit statement distinguishing `red-team` from `reviewer` (pre- vs post-implementation).
- No new pip or build dependencies introduced.

**Done-when:** File exists, all TOML fields are present and consistent with the existing
pattern (`reviewer.toml`, `workflow-architect.toml`), and the role/reviewer distinction
is explicit in the `body`.

---

### Step 2 — Author `.agents/skills/plan-red-team/SKILL.md` and `templates/red-team-findings-template.md`

**Owner:** developer
**Depends on:** Step 1 (role name and return contract settled)
**Write surface:** `.agents/skills/plan-red-team/SKILL.md` (new file), `templates/red-team-findings-template.md` (new file)

These two files are grouped because the SKILL.md references the findings template; writing
them together avoids a half-finished cross-reference.

**Acceptance criteria for SKILL.md (maps to AC-002, R-002, DR-2):**

- File exists at `.agents/skills/plan-red-team/SKILL.md`.
- Begins with `---` YAML frontmatter containing at minimum `name: plan-red-team`, `description:`, and `allowed-tools:` fields, matching the convention of existing skills.
- Process section gives numbered steps covering: reading the work packet (`brief.md`, `plan.md`, `status.md`); identifying challenged assumptions, risks, gaps, and acceptance criteria weaknesses; assigning severity (High/Medium/Low) with source reference to the specific `plan.md` section; stating a suggested resolution per finding; producing one of the three recommendations.
- Guardrails section is present and distinguishes `red-team` output (plan-time findings) from `reviewer` output (post-implementation).
- Done-when section is present and checkable.
- Output section lists: findings document path, structured findings, and recommendation.
- References `templates/red-team-findings-template.md` by path.

**Acceptance criteria for findings template (maps to AC-005, R-005, DR-2, DR-5):**

- File exists at `templates/red-team-findings-template.md`.
- Sections include at minimum: storage / work-id header; review scope (which `plan.md` and review date); findings table or list with fields for finding ID, severity, plan section or claim challenged, concern description, and suggested resolution; overall recommendation (one of approve / revise / escalate); open questions or deferred concerns section.
- Human-readable without tooling (plain Markdown, no special renderer required).
- Follows the structural pattern of `templates/handoff-template.md` (headed sections, fill-in placeholders).

**Done-when:** Both files exist, SKILL.md has correct frontmatter, the template has all
required sections, and SKILL.md references the template by the exact path.

---

### Step 3 — Update `AGENTS.md` and `.agents/project/CLAUDE.md`

**Owner:** developer
**Depends on:** Steps 1 and 2 (role name, description language, and workflow slot settled)
**Write surface:** `AGENTS.md`, `.agents/project/CLAUDE.md`

**Acceptance criteria for AGENTS.md (maps to AC-003, R-003, DR-1):**

- `red-team` appears under **Optional specialists** with a one-line description consistent with `red-team.toml` `body` and explicit about pre-implementation scope.
- `red-team` appears in **Default role flow** as a new numbered entry positioned after `planner` (current step 2) and before `developer` (current step 3), with the condition "on medium/high-risk work" stated.
- Existing step numbers in the default flow are renumbered correctly.
- No other role descriptions are changed.

**Acceptance criteria for `.agents/project/CLAUDE.md` (maps to AC-004, R-004):**

- A new bullet exists under **Working rules** following the pattern of existing specialist bullets (e.g. `workflow-architect`, `technical-writer`).
- Bullet states: invoke `red-team` when the work is medium/high-risk and `planner` has written `plan.md` but before `developer` starts.
- Bullet is consistent with the AC-003 placement in AGENTS.md.

**Done-when:** Both files updated, `red-team` appears at the correct position in AGENTS.md,
and `.agents/project/CLAUDE.md` has a matching when-to-use bullet with no contradicting language.

---

### Verification gate A — Manual AC inspection (after Step 3, before Step 4)

**Owner:** developer (self-check before proceeding to sync)

Read each produced file and confirm each AC is met:

| AC | File | Check |
|---|---|---|
| AC-001 | `.agents/agents/red-team.toml` | All TOML fields present; body covers adversarial intent, invocation trigger, return contract, and reviewer distinction |
| AC-002 | `.agents/skills/plan-red-team/SKILL.md` | Frontmatter present; process steps, guardrails, done-when, output, template reference all present |
| AC-003 | `AGENTS.md` | `red-team` in optional specialists and in default flow at correct position with correct condition |
| AC-004 | `.agents/project/CLAUDE.md` | When-to-use bullet present and consistent with AC-003 |
| AC-005 | `templates/red-team-findings-template.md` | All required sections present; human-readable plain Markdown |

Fix any gap before proceeding to Step 4.

---

### Step 4 — Run `scripts/cli.py sync` and confirm `--check` exits 0

**Owner:** developer
**Depends on:** Verification gate A (ACs 1–5 confirmed)
**Write surface:** Any generated files that `sync` propagates from `.agents/` sources
(e.g. mirrored copies under `.claude/agents/` or similar generated paths)

**Acceptance criteria (maps to AC-006, R-006):**

- `scripts/cli.py sync` runs without error.
- `scripts/cli.py sync --check` exits 0, indicating generated outputs are in sync with sources.
- No unexpected file modifications outside the known generated paths.

**Done-when:** `sync --check` exits 0. If it fails, investigate which source file or
generated target is out of sync, fix it, and re-run.

---

### Step 5 — Add `CHANGELOG.md` entry

**Owner:** developer
**Depends on:** Step 4 (sync confirmed clean)
**Write surface:** `CHANGELOG.md`

**Acceptance criteria (maps to AC-007, R-007):**

- A new bullet appears under the `### Added` heading in the `## [Unreleased]` section.
- Entry names the `red-team` optional specialist role and summarizes what was added (role TOML, `plan-red-team` skill, findings template, AGENTS.md/CLAUDE.md guidance).
- Entry is human-readable and consistent with existing changelog style.
- No entries are moved out of `Unreleased` (no version bump in this step).

**Done-when:** `CHANGELOG.md` has the entry under `Unreleased`; existing entries are
undisturbed; the entry is factually accurate relative to what was produced.

---

### Verification gate B — Final end-to-end check (after Step 5)

**Owner:** developer, then hand back to product-owner

1. Re-run `scripts/cli.py sync --check` — must still exit 0 after CHANGELOG edit.
2. Confirm all seven ACs are met (gate A checklist plus AC-006 and AC-007).
3. Confirm SC-001, SC-002, and SC-003 are satisfied by reading the skill, template, and both TOMLs.
4. Confirm no files outside the declared write surfaces were modified.

**Done-when:** All seven ACs pass, all three BDD scenarios are satisfied on inspection,
`sync --check` exits 0. Developer updates `status.md` and hands back to product-owner.

---

## Parallel lanes

None. Single serial lane. Coordination overhead of parallelism exceeds benefit for this scope.
No worktree isolation needed.

---

## Ownership boundaries

Single developer owns all write surfaces for the duration of this work. No shared state
across concurrent writers.

---

## Blockers / dependencies

None. All decisions are locked in the brief. No external blocking dependencies.

---

## Verification gates

| Gate | Trigger | Check | Pass condition |
|---|---|---|---|
| A | After Step 3 | Manual AC inspection of ACs 1–5 | Each AC met on file inspection |
| B | After Step 5 | Re-run sync --check; full AC + BDD walkthrough | `sync --check` exits 0; all 7 ACs met; SC-001–003 satisfied |

---

## Risks / unknowns

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| `scripts/cli.py sync` propagates files the developer did not anticipate, causing unexpected diffs | Low | Low | Run `sync` in a clean working tree; inspect the diff before committing |
| SKILL.md frontmatter is missing a required field, causing sync or downstream tooling to reject it | Low | Low | Cross-check frontmatter fields against `.agents/skills/requirements-and-traceability/SKILL.md` before running sync |
| Reviewer-vs-red-team distinction is under-described and the two roles feel redundant to adopters | Medium | Medium | Both `body` fields must name the other role's scope explicitly; verify SC-003 before committing |
| AGENTS.md default flow step renumbering introduces off-by-one errors | Low | Low | Recount the default flow list after edit; confirm `planner` stays at 2 and `developer` moves to 4 |

No spikes needed. All risks are low-complexity and addressable inline.

---

## Escalation triggers

Return to product-owner if any of the following occur:

- Any AC is found to be unimplementable as stated.
- The `reviewer` / `red-team` distinction cannot be made clear without changing the brief.
- `scripts/cli.py sync --check` fails in a way that cannot be resolved without touching files outside the declared scope.

---

## Commit strategy

Prefer two atomic commits:

1. `feat(agents): add red-team role, plan-red-team skill, and findings template`
   Covers Steps 1–3 plus any sync-generated files from Step 4.
2. `feat(changelog): record red-team addition under Unreleased`
   Covers Step 5.

If sync produces meaningful generated-file changes distinct from the authoring steps,
those may be committed as a third `chore(sync): regenerate from red-team additions`.

---

## Recommended next owner

**product-owner** — review `plan.md` and approve before developer starts.
