# Product Brief

## Storage

- Work ID: `cli-tools`
- File path: `docs/work/cli-tools/brief.md`

## Request summary

Add a single-entry-point CLI (`scripts/cli.py`) that formalizes the repo's
most repetitive agent-facing processes: scaffolding work packets, scenarios
files, and handoffs; validating work packet structure; listing active work;
and scaffolding new agents and skills.

## Problem / desired outcome

Agents currently construct work packets, handoff files, and scenarios files by
hand from templates — copying paths, numbering handoffs, populating frontmatter.
This is slow, error-prone, and a source of structural drift across work packets.
A CLI that agents can call reduces that friction to a single command and ensures
consistent structure every time.

## Stakeholders / users

- **Agents (primary)** — call the CLI to scaffold and validate; need clean exit
  codes and minimal structured output
- **Humans** — may use `list-work` and `check-work` directly for visibility
- **Downstream adopters** — inherit the CLI with the starter repo

## Stakeholder needs / system outcomes

1. Scaffolding a new work packet takes one command, not manual template copying
2. Handoffs are numbered correctly without agents counting existing files
3. Scenarios files are always placed in the right location from the right template
4. Work packet completeness can be checked mechanically before handoff
5. Active work and ownership is visible at a glance
6. New agents and skills start from a consistent starter template

## In scope

### Tier 1 — scaffolding
- `new-work <work-id>` — create `docs/work/<work-id>/` with `brief.md`,
  `status.md`, `plan.md`, `handoffs/`, `evidence/` from templates
- `new-scenarios [--work <work-id>]` — create `docs/scenarios.md` (no flag)
  or `docs/work/<work-id>/scenarios.md` (with flag) from
  `templates/scenarios-template.md`
- `new-handoff <work-id> --from <role> --to <role>` — create next numbered
  handoff file under `docs/work/<work-id>/handoffs/` from
  `templates/handoff-template.md`, pre-filling work-id, from/to roles, and
  sequence number

### Tier 2 — inspection and agent/skill scaffolding
- `check-work <work-id>` — validate that required sections in `brief.md` and
  `status.md` are non-empty; exit 0 if OK, exit 1 with named gaps if not
- `list-work` — print each work packet with its current owner and current step
  (parsed from `status.md`); exit 0
- `new-agent <name>` — create `.agents/agents/<name>.toml` from a starter
  template with required fields stubbed out
- `new-skill <name>` — create `.agents/skills/<name>/SKILL.md` from a starter
  template with required frontmatter and section headings stubbed out

## Out of scope

- Auto-running the sync script after `new-agent` / `new-skill` (caller's
  responsibility; noted in command output)
- Interactive prompts — all inputs via arguments, no stdin required
- Rich TUI output — plain text only
- JSON output mode (v1; can be added later if agents need structured output)
- Modifying or deleting existing work packets, agents, or skills

## Constraints

- Python 3.x stdlib only — no pip dependencies
- Single entry point: `scripts/cli.py`
- All commands exit 0 on success, non-zero on any error
- `--help` on any subcommand prints usage and exits 0
- Output must be interpretable by an agent reading stdout — concise, labelled,
  no ANSI colour codes
- Must not overwrite existing files — exit 1 with a clear error if the target
  already exists

## Acceptance criteria

**SC-001** — `python scripts/cli.py new-work foo` creates `docs/work/foo/`
with `brief.md`, `status.md`, `plan.md`, `handoffs/`, and `evidence/`
populated from their templates. Running it again on the same ID exits 1 with
"already exists".

**SC-002** — `python scripts/cli.py new-scenarios --work foo` creates
`docs/work/foo/scenarios.md` from `templates/scenarios-template.md`.
Without `--work` it creates `docs/scenarios.md`.

**SC-003** — `python scripts/cli.py new-handoff foo --from planner --to developer`
creates `docs/work/foo/handoffs/001-planner-to-developer.md` (or the next
available sequence number if earlier handoffs exist) from
`templates/handoff-template.md` with work-id, from, to, and sequence
pre-filled.

**SC-004** — `python scripts/cli.py check-work foo` exits 0 when all required
sections in `brief.md` and `status.md` have non-placeholder content; exits 1
and lists the missing/empty sections when any are incomplete.

**SC-005** — `python scripts/cli.py list-work` prints one line per work packet
showing work-id, current owner, and current step (or "unknown" when the field
cannot be parsed). Exit 0 even when no work packets exist.

**SC-006** — `python scripts/cli.py new-agent foo` creates
`.agents/agents/foo.toml` with all required TOML fields stubbed; prints a
reminder to run `python scripts/sync_agent_layouts.py` afterwards.

**SC-007** — `python scripts/cli.py new-skill foo` creates
`.agents/skills/foo/SKILL.md` with required frontmatter and section headings
stubbed; prints the same sync reminder.

**SC-008** — `python scripts/cli.py --help` and `python scripts/cli.py
<subcommand> --help` both exit 0 with usage text.

## Delivery class

Non-productized tool. TDD not required; explicit verification against the
acceptance criteria before closing.

## TDD expectation

Not required. Verification: run each subcommand against a temp directory and
confirm exit codes and file contents match the acceptance criteria.

## SemVer / changelog expectation

**MINOR** — new tooling. CHANGELOG `Added` entry.

## Assumptions

- Templates already exist for brief, status, plan, handoff, and scenarios
- `docs/work/` may or may not exist when CLI is first run; CLI creates it
- Sequence numbering for handoffs: scan `handoffs/` for `NNN-*` files, take
  max N + 1, zero-pad to 3 digits
- `check-work` required sections: all `##` headings in brief.md and status.md
  whose body is either empty or still contains the template placeholder text
  (detected by the presence of angle-bracket tokens like `<work-id>`)
- `list-work` parses `## Current owner` → `- Role:` and `## Current step`
  lines from `status.md` using simple line scanning, not a Markdown parser

## Open questions

1. **Starter template for `new-agent`**: full body stub or minimal? Propose
   minimal (name, description, tools, body placeholder) — planner to confirm.
2. **`new-work` template population**: replace `<work-id>` placeholder tokens
   in templates automatically? Yes — planner to confirm the replacement set.
3. **`check-work` strictness**: flag sections that still contain `<work-id>`
   placeholder tokens as incomplete, or only flag entirely empty sections?
   Propose: flag placeholder tokens as incomplete — planner to confirm.

## Recommended next owner

`planner` — resolve open questions, sequence the subcommands, define the
verification fixture shape, and write `plan.md`.
