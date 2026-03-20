# Work Plan

## Storage

- Work ID: `scenario-traceability`
- File path: `docs/work/scenario-traceability/plan.md`
- Source brief: `docs/work/scenario-traceability/brief.md`

## Problem statement

No convention exists in this starter repo for plain-English usage scenarios with
stable IDs linked to tests. Scenario → test traceability is currently implicit
at best, absent in practice. This plan adds the convention, a template, a
coverage script, guidance wiring, and a verifiable fixture set.

## Stakeholders / system context

- Product owners write scenarios; developers write tests; verifiers run the script
- Downstream teams inherit the convention from the starter repo
- The script is repo-root-agnostic (runs from any directory via `--root`)

## Scope

- `templates/scenarios-template.md`
- `scripts/check-scenario-coverage.py`
- `tests/fixtures/scenario-traceability/` — three fixture cases
- `.agents/skills/scenario-traceability/SKILL.md` (canonical; synced to `.claude/skills/`)
- `.agents/rules/scenario-traceability.md` (canonical; synced to `.claude/rules/`)
- Migrate existing 4 rule files from `.claude/rules/` to `.agents/rules/` (makes system consistent)
- Extend `scripts/sync_agent_layouts.py` with `copy_rules()` to sync `.agents/rules/` → `.claude/rules/`
- Update `agents-and-generation.md` rule to name `.agents/rules/` as canonical source
- One bullet added to `.agents/project/CLAUDE.md` §Working rules (synced to `.claude/CLAUDE.md`)
- Cross-reference paragraph added to `.agents/skills/bdd/SKILL.md` and
  `.agents/skills/requirements-and-traceability/SKILL.md`
- CHANGELOG.md entry

## Non-goals

- CI wiring (per-project concern, out of scope)
- `--update-table` flag (v2)
- Gherkin, test-framework adapters, or code generation
- Renaming or removing any existing artifact

## Requirements / constraints / assumptions to keep visible

- Script: Python 3.x, stdlib only, no pip deps
- IDs: template enforces `SC-NNN` (3-digit zero-padded); script regex is `SC-\d+` (tolerant)
  — `SC-1` and `SC-001` are distinct IDs; the template is authoritative on format
- `scripts/` directory already exists (contains `sync_agent_layouts.py`)
- Trace table: human-maintained in v1; script is read-only
- Convention must not contradict existing `bdd` or `requirements-and-traceability` guidance
- `.agents/` is the canonical source for all skills, rules, and CLAUDE.md;
  `.claude/` is generated output — never hand-edit `.claude/` directly
- Migrating existing rule files to `.agents/rules/` is in scope — `copy_rules()`
  must handle cleanup (delete stale `.claude/rules/` files not in `.agents/rules/`)
  so the system stays consistent

## Public contract / compatibility impact

Additive only. No existing file is renamed, moved, or deleted. New files:
- `templates/scenarios-template.md`
- `scripts/check-scenario-coverage.py`
- `.claude/rules/scenario-traceability.md`
- `tests/fixtures/scenario-traceability/` (three sub-cases)

## SemVer / changelog expectation

**MINOR** — new templates, tooling, and guidance. CHANGELOG.md `Added` entry.

## Key behavior rules / scenarios

From brief — binding:

| ID     | Behavior |
|--------|----------|
| SC-001 | Scenarios file is readable plain English; each entry has unique `SC-NNN` ID |
| SC-002 | `Covers: SC-NNN` in a test file is recognized as covering that scenario |
| SC-003 | Any uncovered scenario → non-zero exit + named in output |
| SC-004 | All scenarios covered → zero exit |
| SC-005 | Orphaned test reference (no matching scenario) → non-zero exit + named |
| SC-006 | Script auto-discovers both `docs/scenarios.md` and `docs/work/*/scenarios.md` |
| SC-007 | Template + rule file are self-contained; no work-packet reading required |
| SC-008 | Trace table format (GFM) maps SC-NNN → test file(s) |

## Resolved open questions

1. **Script output format**: plain text to stdout. Format:
   ```
   Scanning 2 scenario file(s), 5 test file(s)...

   UNCOVERED SCENARIOS:
     SC-002  [docs/scenarios.md] The device validates sample rate on startup

   ORPHANED REFERENCES:
     SC-999  tests/unit/test_foo.c (not defined in any scenarios file)

   Result: 3 covered, 1 uncovered, 1 orphaned — FAIL
   ```
   Clean run: `Result: 4 covered, 0 uncovered, 0 orphaned — OK`

2. **`--update-table` flag**: deferred to v2. Script is read-only in v1.

3. **ID zero-padding**: template convention = `SC-NNN` minimum 3 digits.
   Script regex = `SC-\d+` (tolerant). `SC-1` ≠ `SC-001` — they are distinct.
   Template is the authoritative form; the script does not coerce.

4. **Guidance location**: `.claude/rules/scenario-traceability.md` (new file).
   One cross-reference bullet added to CLAUDE.md §Working rules.
   Cross-reference paragraph appended to `bdd` and `requirements-and-traceability` skills.

## Script CLI interface

```
python scripts/check-scenario-coverage.py [OPTIONS]

Options:
  --root DIR      Repo root to resolve globs from (default: current directory)
  --tests GLOB    Glob for test files relative to root
                  (default: tests/**/* — all files under tests/)
  --help          Print usage and exit 0

Auto-discovered scenario files (relative to root, always):
  docs/scenarios.md
  docs/work/*/scenarios.md

Exit codes:
  0  All scenarios covered AND no orphaned references
  1  One or more uncovered scenarios OR orphaned references found

Output: plain text to stdout
```

The script does NOT take an explicit `--scenarios` flag in v1. Auto-discovery
is fixed to the two canonical paths. The `--tests` glob is the only configurable
input surface for v1.

## Fixture structure

```
tests/fixtures/scenario-traceability/
  all-covered/                        # SC-004, SC-006 — dual scope, zero exit
    docs/
      scenarios.md                    # SC-001, SC-002
      work/
        feat-a/
          scenarios.md                # SC-001 (independent scope in feat-a)
    tests/
      test_main.c                     # // Covers: SC-001 \n // Covers: SC-002
      test_feature.py                 # # Covers: SC-001  (covers feat-a SC-001)

  gap/                                # SC-003 — one uncovered, non-zero exit
    docs/
      scenarios.md                    # SC-001, SC-002, SC-003
    tests/
      test_main.c                     # // Covers: SC-001 \n // Covers: SC-002
      # SC-003 has no test reference

  orphan/                             # SC-005 — orphaned reference, non-zero exit
    docs/
      scenarios.md                    # SC-001
    tests/
      test_main.c                     # // Covers: SC-001 \n // Covers: SC-999
      # SC-999 not defined in any scenarios file
```

Each fixture case is exercised by running the script with `--root <case-dir>`.

## Preferred test strategy

Non-productized tool — explicit verification via fixture cases rather than TDD.
Fixture cases map directly to acceptance criteria. A verification record is
written after fixture runs pass, confirming each SC-001–SC-008.

## Validation plan

Requester reviews the rendered `templates/scenarios-template.md` and a sample
scenarios file before work is closed. Validation question: "Would you actually
write this? Would a developer add `Covers: SC-NNN` without friction?"

## Walking skeleton

Minimal testable slice: script + `gap/` fixture → non-zero exit. That single
check demonstrates the core detection loop before the other cases are written.

## Plan steps

### Pre-conditions (confirmed)
- [x] Brief approved and open questions resolved (this document)
- [x] `scripts/` directory exists
- [x] `.agents/` canonical layout understood; sync script reviewed

### Step 1 — Template
Write `templates/scenarios-template.md`.
- Sections: header, how-to-use comment, project-level example (SC-001, SC-002),
  trace table skeleton, guidance on ID assignment
- ≤ 60 lines
- Not synced — templates live in `templates/` directly, not under `.agents/`

### Step 2 — Extend sync script to handle rules
Extend `scripts/sync_agent_layouts.py` with a `copy_rules()` function:
- Source: `.agents/rules/*.md`
- Destination: `.claude/rules/*.md`
- Same copy + cleanup pattern as `copy_skills()` — deletes stale `.claude/rules/`
  files not present in `.agents/rules/`
- Add `copy_rules(...)` call in `main()` alongside `copy_skills(...)`
- `--check` flag must cover rules the same as skills

### Step 3 — Migrate existing rule files to `.agents/rules/`
Move (copy then verify) the four existing `.claude/rules/*.md` files to
`.agents/rules/`:
- `agents-and-generation.md`
- `docs-and-contract.md`
- `claude-runtime.md`
- `parallel-lanes.md`
Update `agents-and-generation.md` canonical source to name `.agents/rules/` as
the canonical location for rules.
Run `python scripts/sync_agent_layouts.py` → regenerates `.claude/rules/`
from `.agents/rules/`. Confirm the four files are identical to the originals.

### Step 4 — New skill (canonical)
Write `.agents/skills/scenario-traceability/SKILL.md`.
- Describes: when to write scenarios, ID format, test reference syntax,
  trace table, how to run the coverage script, link to template
- Same structure as existing skills (frontmatter + sections)
- Run `python scripts/sync_agent_layouts.py` → propagates to
  `.claude/skills/scenario-traceability/SKILL.md`

### Step 5 — New rule (canonical)
Write `.agents/rules/scenario-traceability.md`.
- Path-scoped to `docs/scenarios.md`, `docs/work/*/scenarios.md`, `tests/**/*`
- Content: quick-ref for ID format, test reference syntax, script invocation
- Run sync → produces `.claude/rules/scenario-traceability.md`

### Step 6 — CLAUDE.md pointer (canonical)
Add one bullet to `.agents/project/CLAUDE.md` §Working rules:
```
- Use the `scenario-traceability` skill to keep plain-English usage scenarios
  linked to tests with mechanical coverage checking.
```
Run sync → propagates to `.claude/CLAUDE.md`.

### Step 7 — Skill cross-references (canonical)
Append a cross-reference to two skills in `.agents/skills/`:
- `bdd/SKILL.md`: "When scenarios are stable, assign `SC-NNN` IDs and wire
  coverage using the `scenario-traceability` skill."
- `requirements-and-traceability/SKILL.md`: same cross-reference.
Run sync → propagates both to `.claude/skills/`.

### Step 8 — Coverage script (walking skeleton first)
Write `scripts/check-scenario-coverage.py`.
- Walking skeleton: parse `gap/` fixture, detect uncovered scenario, exit 1 → Gate G1
- Expand to full: all-covered exits 0; orphan exits 1 with correct output
- Stdlib only (`pathlib`, `re`, `sys`, `argparse`)
- Shebang: `#!/usr/bin/env python3`

### Step 9 — Fixtures
Write all three fixture cases under `tests/fixtures/scenario-traceability/`.
- `all-covered/` — exercises SC-004 and SC-006 (dual scope discovery)
- `gap/` — exercises SC-003 (uncovered scenario)
- `orphan/` — exercises SC-005 (orphaned reference)

### Step 10 — Verification
Run each fixture case. Record results in
`docs/work/scenario-traceability/evidence/verification.md`.
Map each run to SC-001–SC-008. All must pass.

```sh
python scripts/check-scenario-coverage.py \
  --root tests/fixtures/scenario-traceability/all-covered
# expected: exit 0

python scripts/check-scenario-coverage.py \
  --root tests/fixtures/scenario-traceability/gap
# expected: exit 1, names uncovered scenario

python scripts/check-scenario-coverage.py \
  --root tests/fixtures/scenario-traceability/orphan
# expected: exit 1, names orphaned SC-NNN
```

Also run: `python scripts/sync_agent_layouts.py --check` → exit 0 (all
generated files in sync).

### Step 11 — Validation gate
Present `templates/scenarios-template.md` and sample script output to requester.
Explicit confirmation required before committing.

### Step 12 — CHANGELOG.md

### Step 13 — Commits (three, one logical change each)
1. `feat(sync): extend sync script to copy rules from .agents/rules/`
   — sync script extension + rule migration
2. `feat(traceability): add scenario-traceability skill, rule, and guidance`
   — skill + rule + CLAUDE.md bullet + skill cross-refs + template
3. `feat(traceability): add coverage script and verification fixtures`
   — script + fixtures + verification record + CHANGELOG.md

## Parallel lanes

None in this execution (single-thread option A). Lanes A and B were identified
as separable in the brief but sequencing them is simpler and lower risk here.
If this work is done in a future parallel setup, Lane A = steps 1–4,
Lane B = steps 5–6, merge after step 6 before verification.

## Ownership boundaries

Single owner throughout (product-owner wearing planner + developer + verifier
hats in sequence). Validation gate (step 8) hands back to requester.

## Blockers / dependencies

None. No external dependencies. `scripts/` already exists.

## Verification gates

| Gate | After step | Check | Pass condition |
|------|-----------|-------|----------------|
| G0   | Step 3 | `python scripts/sync_agent_layouts.py --check` | exit 0; migrated rules identical |
| G1   | Step 8 (skeleton) | `python scripts/check-scenario-coverage.py --root .../gap` | exit 1, uncovered scenario named |
| G2   | Step 9 | all-covered exits 0, orphan exits 1 | both pass |
| G3   | Step 10 | verification record complete + `sync --check` exit 0 | SC-001–SC-008 all checked |
| G4   | Step 11 | requester approves template | explicit confirmation |

## Risks / unknowns

- **glob behavior on `docs/work/*/scenarios.md`**: Python's `pathlib.glob` and
  `glob.glob` handle `*` differently with nested paths. Use `pathlib.Path.glob`
  which handles `*/` correctly. Low risk, verify in fixture run.
- **Template length**: keeping it ≤ 60 lines with meaningful examples is tight.
  If it needs to be longer for clarity, prefer clarity over the line limit.
- **Skill cross-references**: appending to existing SKILL.md files is a
  behavioral change to published guidance. Keep additions minimal (≤ 3 lines)
  and clearly additive.
- **Rule migration**: `copy_rules()` cleanup will delete `.claude/rules/` files
  not in `.agents/rules/`. Migrating all four existing rules before running sync
  is critical — wrong order would delete them. Steps 2→3 order is enforced.

## Escalation triggers

- If `pathlib.glob` does not handle `docs/work/*/scenarios.md` correctly on the
  target platform → escalate to product-owner before shipping the script
- If requester rejects template at validation gate → return to product-owner
  for a design revision before committing anything
