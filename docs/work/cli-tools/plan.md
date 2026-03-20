# Work Plan

## Storage

- Work ID: `cli-tools`
- File path: `docs/work/cli-tools/plan.md`
- Source brief: `docs/work/cli-tools/brief.md`

## Problem statement

Agents and humans currently construct work packets, handoff files, and
scenarios files by hand from templates. This is slow, error-prone, and
produces structural drift. `scripts/cli.py` must provide eight subcommands
that reduce every repetitive scaffolding and inspection task to a single
invocable command with clean exit codes and interpretable stdout.

The work is done when all eight subcommands exist, SC-001 through SC-008
pass against a temporary directory, and `CHANGELOG.md` has a new `Added`
entry.

## Delivery class

Non-productized tool. TDD is not required. Replacement verification:
run each acceptance scenario against a temp directory, confirm exit codes
and file contents, and record the evidence before closing.

## Stakeholders / system context

- **Agents (primary)** — invoke the CLI; depend on exit codes and
  machine-interpretable stdout
- **Humans** — use `list-work` and `check-work` directly
- **Downstream adopters** — inherit the CLI with the starter repo starter kit
- **Repo contract consumers** — `scripts/cli.py` becomes a new documented
  entry point; its subcommand names and exit-code semantics are the public
  surface

System context: pure host-side Python script, no build system, no pip
dependencies, no hardware. Depends only on Python 3.x stdlib and the
repo's existing template files under `templates/`.

## Scope

All eight subcommands as defined in the brief (SC-001 through SC-008):
`new-work`, `new-scenarios`, `new-handoff`, `check-work`, `list-work`,
`new-agent`, `new-skill`, and `--help` on all subcommands.

## Non-goals

- Auto-running `sync_agent_layouts.py` after `new-agent` / `new-skill`
- Interactive prompts or stdin
- ANSI colour output
- JSON output mode
- Modifying or deleting existing files
- Any subcommand not listed in the brief

## Resolved open questions

### OQ-1: new-agent starter template depth

**Decision: minimal stub.**

The generated `.agents/agents/<name>.toml` will include:

```toml
name = "<name>"
description = "# TODO: describe this agent"
tools = []
skills = []
claude_max_turns = 20
body = """
# TODO: describe role responsibilities, optimizations, and return contract.
"""
```

Rationale: the caller needs to fill in role-specific content regardless.
Codex-specific fields (`codex_model_reasoning_effort`, `codex_sandbox_mode`,
`codex_nickname_candidates`) are omitted from the stub to avoid requiring
the caller to understand Codex semantics before they are relevant.

### OQ-2: new-work placeholder replacement set

**Decision: replace `<work-id>` only.**

When scaffolding a new work packet, the CLI substitutes `<work-id>` with
the supplied work-id argument in all copied template files. All other
`<...>` tokens are content prompts left for the author; they are not
structural references and must not be silently replaced.

Affected template files for `new-work`:
- `templates/product-brief-template.md` → `docs/work/<work-id>/brief.md`
- `templates/work-plan-template.md` → `docs/work/<work-id>/plan.md`
- `templates/work-status-template.md` → `docs/work/<work-id>/status.md`
- `handoffs/` and `evidence/` created as empty directories (no file copied)

### OQ-3: check-work strictness

**Decision: flag any section whose body still contains an angle-bracket
token (`<...>`) as incomplete, in addition to sections with an empty body.**

A section with only whitespace, or whose non-blank content contains at
least one `<token>` match, is reported as unfilled. This catches
template placeholders that were not replaced, which is the most common
form of structural drift.

Detection rule per `##`-level section in `brief.md` and `status.md`:
extract the text between the heading line and the next `##` heading (or
EOF); strip whitespace; if empty OR if it matches `<[^>]+>` anywhere,
report it as incomplete.

## Public contract / compatibility impact

`scripts/cli.py` becomes a new repo contract surface. The subcommand
names, required arguments, and exit-code semantics documented in SC-001
through SC-008 are the v1 public interface. Adding subcommands later is a
MINOR change. Renaming a subcommand or changing an exit-code meaning is a
MAJOR change.

No existing repo contract surfaces change in this work.

## SemVer / changelog expectation

**MINOR** — new tooling, backward-compatible addition. `CHANGELOG.md`
requires a new `Added` entry under `Unreleased`.

## Key behavior rules / scenarios

Scenarios are the acceptance criteria SC-001 through SC-008 from the
brief. They are reproduced here with test-level assignments:

| ID     | Scenario summary                           | Test level          |
|--------|--------------------------------------------|---------------------|
| SC-001 | new-work creates packet; idempotent exit 1 | Functional (temp dir) |
| SC-002 | new-scenarios with/without --work flag     | Functional (temp dir) |
| SC-003 | new-handoff sequential numbering           | Functional (temp dir) |
| SC-004 | check-work exit codes and gap reporting    | Functional (temp dir) |
| SC-005 | list-work prints owner+step; tolerates empty | Functional (temp dir) |
| SC-006 | new-agent creates stub TOML + sync reminder | Functional (temp dir) |
| SC-007 | new-skill creates stub SKILL.md + sync reminder | Functional (temp dir) |
| SC-008 | --help exits 0 on all subcommands          | Functional (temp dir) |

All scenarios are host-only (no hardware). All run at the functional
script level by driving `scripts/cli.py` as a subprocess from a temp
directory.

## Trade studies / decision points

No open trade studies. Key decisions were locked in the brief (single
entry point, stdlib only, no TDD, temp-dir verification).

The OQ-1 / OQ-2 / OQ-3 resolutions above are the remaining decisions.
No further trade study is needed before implementation.

## Preferred test strategy

Verification replaces TDD for this non-productized tool. The developer
will write a `tests/test_cli.py` script (or equivalent) that:

1. Creates a fresh `tempfile.TemporaryDirectory` per scenario.
2. Copies the repo's `templates/` into the temp tree so the CLI can
   find its source templates via a `--root` flag or by locating the
   repo root from `__file__`.
3. Drives each SC scenario as a subprocess (`python scripts/cli.py …`).
4. Asserts on return code, filesystem contents, and stdout.
5. Tears down the temp directory after each scenario.

**Fixture approach: temp directory (not a committed fixture dir).** Each
test creates its own isolated tree. This avoids fixture drift and makes
every scenario self-contained.

The developer must run all eight scenario checks and record pass/fail
evidence before handing to verifier. The verifier re-runs the checks
independently and confirms.

The `check-scenario-coverage.py` tool is not invoked here because
`scripts/cli.py` is a tool, not a product behavior being traced to
firmware scenarios.

## Validation plan

Validation is not a meaningful concern for this slice. The primary users
(agents and repo maintainers) will know immediately whether the CLI
works by running it. No separate stakeholder-fit evidence is required
beyond the functional verification of SC-001 through SC-008.

## Walking skeleton

**Step 1** (first deliverable): `scripts/cli.py` parses `--help` and one
subcommand (`new-work`) end-to-end: creates the directory tree, copies
and patches templates, refuses to overwrite. This proves the argparse
wiring, template-finding logic, and `<work-id>` substitution work before
the remaining six subcommands are added.

## Minimal configuration / iteration target

All eight subcommands in a single serial lane. The tool is small enough
that parallelism would add coordination overhead without saving calendar
time.

## Exit criteria / milestone criteria

- `scripts/cli.py` exists and is executable with `python scripts/cli.py`
- SC-001 through SC-008 each produce the described filesystem state and
  exit codes when run against a temp directory
- Verification evidence is recorded under
  `docs/work/cli-tools/evidence/`
- `CHANGELOG.md` has an `Added` entry under `Unreleased`
- `status.md` is updated to reflect the current owner

## Plan steps

### Step 0 — Scaffold `docs/work/cli-tools/scenarios.md`

Owner: developer  
Depends on: nothing  
Done when: `docs/work/cli-tools/scenarios.md` lists SC-001 through
SC-008 with the scenario text from the brief, ready for `Covers:`
annotations.

Acceptance criteria:
- File exists at `docs/work/cli-tools/scenarios.md`
- All eight SC IDs appear with their brief description text
- Trace table is present (initially all Uncovered)

---

### Step 1 — Entry-point wiring and `--help` (SC-008)

Owner: developer  
Depends on: Step 0  
Done when: `scripts/cli.py` exists with an `argparse` subparser for
every subcommand name; `python scripts/cli.py --help` and
`python scripts/cli.py <subcommand> --help` each exit 0 and print usage.
No subcommand has any implementation beyond printing "not yet
implemented".

Acceptance criteria:
- SC-008 passes (all `--help` invocations exit 0)
- All eight subcommand names are registered (even if unimplemented)
- Unknown subcommands exit non-zero

---

### Step 2 — `new-work` (SC-001)

Owner: developer  
Depends on: Step 1  
Done when: `new-work <id>` creates `docs/work/<id>/` with `brief.md`,
`plan.md`, `status.md`, `handoffs/`, `evidence/` copied from templates
with `<work-id>` replaced; running it again exits 1 with "already
exists".

Acceptance criteria:
- SC-001 passes in a temp directory
- All three template files are present with `<work-id>` replaced
- `handoffs/` and `evidence/` directories exist
- Second invocation exits 1 and names the conflict

---

### Step 3 — `new-scenarios` (SC-002)

Owner: developer  
Depends on: Step 1  
Done when: `new-scenarios` creates `docs/scenarios.md`; `new-scenarios
--work <id>` creates `docs/work/<id>/scenarios.md`; both exit 1 if the
file already exists.

Acceptance criteria:
- SC-002 passes in a temp directory (both with and without `--work`)
- Content matches `templates/scenarios-template.md`
- Duplicate invocation exits 1

Steps 2 and 3 are independent of each other and could be written in
parallel, but given the small size of the work, they are kept serial to
avoid coordination overhead.

---

### Step 4 — `new-handoff` (SC-003)

Owner: developer  
Depends on: Step 2 (the `handoffs/` directory convention is established
by `new-work`; the implementation logic is independent but the test
fixture benefits from a populated work packet)  
Done when: `new-handoff <id> --from <role> --to <role>` creates the
next numbered file; sequence numbering scans for `NNN-*` files, takes
max+1, zero-pads to 3 digits; pre-fills work-id, roles, and sequence
in the file.

Acceptance criteria:
- SC-003 passes: first handoff creates `001-<from>-to-<to>.md`
- Second invocation with different roles creates `002-...`
- Content has `<work-id>`, `<from>`, `<to>`, and sequence pre-filled
- Missing `handoffs/` directory exits 1 with a clear error

---

### Step 5 — `check-work` (SC-004)

Owner: developer  
Depends on: Step 2 (uses `brief.md` and `status.md` as input)  
Done when: `check-work <id>` exits 0 when all `##` sections have
non-placeholder content; exits 1 and names each incomplete section when
any `##` section body is empty or still contains `<...>` tokens.

Acceptance criteria:
- SC-004 passes: clean packet exits 0; template-fresh `brief.md` exits
  1 with each unfilled section listed by heading name
- The `<work-id>` token introduced by OQ-3 detection is treated as
  incomplete
- Missing work packet exits 1 with "not found"

---

### Step 6 — `list-work` (SC-005)

Owner: developer  
Depends on: Step 2 (to have a realistic status.md to parse)  
Done when: `list-work` prints one line per work packet in
`docs/work/*/` showing `<work-id>  owner: <role>  step: <text>`;
"unknown" substituted when a field cannot be parsed; exits 0 even when
no packets exist.

Acceptance criteria:
- SC-005 passes with zero, one, and two work packets in the temp tree
- Owner parsed from `## Current owner` / `- Role:` line in `status.md`
- Step parsed from the line following `## Current step` in `status.md`
- "unknown" for any field that cannot be parsed (malformed or absent)

---

### Step 7 — `new-agent` and `new-skill` (SC-006, SC-007)

Owner: developer  
Depends on: Step 1  
Done when:
- `new-agent <name>` creates `.agents/agents/<name>.toml` with the
  minimal stub defined in OQ-1; prints sync reminder; exits 1 if
  file exists
- `new-skill <name>` creates `.agents/skills/<name>/SKILL.md` with
  required frontmatter (`name`, `description`, `allowed-tools`) and
  section headings (`# <Name>`, `## Process`, `## Done-when`,
  `## Output`) stubbed; prints sync reminder; exits 1 if file exists

Acceptance criteria:
- SC-006 passes: TOML has `name`, `description`, `tools`, `skills`,
  `claude_max_turns`, `body` fields; sync reminder printed to stdout
- SC-007 passes: SKILL.md has YAML frontmatter and four required
  headings; sync reminder printed to stdout
- Duplicate invocation exits 1 on both

---

### Step 8 — Verification pass (SC-001 through SC-008)

Owner: developer, then verifier  
Depends on: Steps 1–7  
Done when: a `tests/test_cli.py` script (or inline shell-driven record)
drives all eight SC scenarios against a temp directory, records actual
exit codes and sampled file contents, and the verifier independently
re-runs the checks and confirms.

Acceptance criteria:
- All eight SCs pass with documented exit codes and file content samples
- Evidence recorded under `docs/work/cli-tools/evidence/`
- `Covers: SC-NNN` comment in the test for each scenario
- `docs/work/cli-tools/scenarios.md` trace table updated

---

### Step 9 — Changelog and status update

Owner: developer  
Depends on: Step 8  
Done when: `CHANGELOG.md` has an `Added` entry for `scripts/cli.py`
under `Unreleased`; `status.md` reflects the completed state.

Acceptance criteria:
- `CHANGELOG.md` entry is human-readable and names the eight subcommands
- `status.md` current owner set to `verifier` or `product-owner`
  depending on handoff

## Parallel lanes

No parallel lanes. The work is a single script small enough that
parallel writes would add integration overhead with no calendar benefit.
All steps are serial in the order above.

## Ownership boundaries

- Developer owns Steps 0–9.
- Verifier owns independent re-execution in Step 8.
- Product-owner approves this plan before Step 1 begins and receives
  the Step 8 evidence before sign-off.

## Blockers / dependencies

- Templates must exist before Step 1. All required templates
  (`templates/product-brief-template.md`, `templates/work-plan-template.md`,
  `templates/work-status-template.md`, `templates/handoff-template.md`,
  `templates/scenarios-template.md`) already exist in the repo. No
  blocker.
- Python 3.x must be available on the host. Assumed present. No blocker.

## Verification gates

| Gate | After step | Check |
|------|-----------|-------|
| V1 | Step 1 | `--help` on all subcommands exits 0 |
| V2 | Step 7 | All eight subcommands executable without errors |
| V3 | Step 8 | All SC-001 through SC-008 pass, evidence recorded |
| V4 | Step 9 | CHANGELOG updated, status.md updated |

Developer self-checks at V1 and V2. Verifier independently re-runs V3.
Product-owner reviews V4 before closing.

## Risks / unknowns

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Template `<work-id>` tokens appear in unexpected positions (e.g. code blocks) | Low | OQ-2 pins replacement to exact `<work-id>` string; regression caught by SC-001 content check |
| `check-work` angle-bracket detection produces false positives (e.g. HTML tags in a brief) | Low | Detection is on `##`-section bodies only; brief template has no HTML; add test case with non-placeholder angle bracket if it surfaces |
| Sequence numbering race (two agents call `new-handoff` simultaneously) | Very low (single-user tool) | Not in scope; document as known limitation |
| `list-work` parser breaks on future changes to `status.md` template | Medium | Parser is line-scan only; document the two expected heading formats as a fixed contract |

## Escalation triggers

- Brief acceptance criteria are unclear or contradictory → return to product-owner
- A required template is missing or structurally different from what the
  CLI expects → return to product-owner
- OQ resolutions above conflict with a real use case found during
  implementation → return to planner before continuing
