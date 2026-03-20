# Handoff

## Storage

- Work ID: `scenario-traceability`
- File path: `docs/work/scenario-traceability/handoffs/001-product-owner-to-planner.md`
- Packet root: `docs/work/scenario-traceability/`

## From

- Agent: product-owner
- Date: 2026-03-20

## To

- Agent: planner

## Handoff rationale

- Why this role is the right next owner: The brief is approved and all four
  design decisions are locked by the requester. The next job is to sequence
  the deliverables, resolve the four open questions, decide the script
  interface and fixture shape, and produce a checkable plan before any
  implementation begins. That is planner's lane.

## Canonical context

- Brief: `docs/work/scenario-traceability/brief.md`
- Plan: `docs/work/scenario-traceability/plan.md` _(to be created)_
- Status: `docs/work/scenario-traceability/status.md`
- Evidence touched: none yet

## Delta since last checkpoint

- What changed: work packet created from scratch; brief written and confirmed
  with requester
- New decisions (confirmed by requester):
  1. Scenarios live at both project level (`docs/scenarios.md`) and work-packet
     level (`docs/work/<work-id>/scenarios.md`)
  2. Format: plain English — no Gherkin
  3. Traceability: both `Covers: SC-NNN` in test code AND a trace table doc
  4. Coverage must be mechanically verifiable (script, non-zero exit on gaps)
- New or changed assumptions: see brief §Assumptions
- New or changed risks / blockers: none
- Files or artifacts added / updated:
  - `docs/work/scenario-traceability/brief.md` (new)
  - `docs/work/scenario-traceability/status.md` (new)
  - `docs/work/scenario-traceability/handoffs/001-product-owner-to-planner.md` (this file)

## Context the recipient must preserve

- Requester's four confirmed decisions are binding — do not re-open them
- SC-NNN IDs must be stable (no renumbering on insert); this constraint drives
  the ID assignment and script parsing approach
- The script must be language-agnostic (comment-based, not AST-based)
- Python 3.x is the preferred script language over shell for robustness
- The trace table is informational; the script is the authoritative coverage check
- Validation requires requester to review the template and sample scenarios
  before the work is closed — keep that gate explicit in the plan

## Parallel work context

- Lane / owner: no parallel lanes yet; planner decides after locking the interface
- Dependencies: Lane A (template + docs) and Lane B (script + fixture) can
  potentially be parallelized once conventions are locked
- Integration checkpoint: product-owner reviews plan before implementation starts

## Evidence gathered so far

None — brief is the only artifact.

## Impact analysis / downstream effects

- Requirements / design criteria affected: brief §Acceptance criteria SC-001–SC-008
- Interfaces / components affected: `templates/`, `scripts/`, `CLAUDE.md` or
  `AGENTS.md`, possibly one or two skills
- Verification / validation / docs affected: new fixture needed; requester
  review of template required

## Requested next action

1. Read `brief.md` in full
2. Resolve the four open questions (brief §Open questions)
3. Decide parallelization: single lane or Lane A + Lane B?
4. Define the script CLI interface (arguments, flags, output format, exit codes)
5. Define the fixture structure for verifying SC-001 through SC-008
6. Write `plan.md`
7. Return `plan.md` to product-owner for lane approval before implementation

## Done-when

- `plan.md` exists with a sequenced step list, parallel lane decision, script
  interface definition, fixture shape, and all four open questions resolved
- product-owner has approved the plan
