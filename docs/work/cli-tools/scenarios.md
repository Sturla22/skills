# Usage Scenarios

<!-- Work-packet: docs/work/cli-tools/scenarios.md -->

<!-- HOW TO USE                                                               -->
<!-- 1. Add one scenario per entry. Keep the language non-technical.          -->
<!-- 2. Assign the next available SC-NNN ID. Never renumber existing entries. -->
<!-- 3. In each covering test add a comment: Covers: SC-NNN                   -->
<!-- 4. Run `python scripts/check-scenario-coverage.py` to verify coverage.  -->
<!-- 5. Update the trace table below when you add or cover a scenario.        -->

## Scenarios

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

<!-- Add new scenarios below. Use the next integer; do not reuse or renumber. -->

## Trace table

<!-- Updated by hand or regenerated with: python scripts/check-scenario-coverage.py --root . -->
<!-- Status: Covered | Uncovered | Partial                                    -->

| ID     | Description (short)                         | Covering test(s) | Status    |
|--------|---------------------------------------------|------------------|-----------|
| SC-001 | new-work creates packet; idempotent exit 1  | —                | Uncovered |
| SC-002 | new-scenarios with/without --work flag      | —                | Uncovered |
| SC-003 | new-handoff sequential numbering            | —                | Uncovered |
| SC-004 | check-work exit codes and gap reporting     | —                | Uncovered |
| SC-005 | list-work prints owner+step; tolerates empty | —               | Uncovered |
| SC-006 | new-agent creates stub TOML + sync reminder | —                | Uncovered |
| SC-007 | new-skill creates stub SKILL.md + sync reminder | —            | Uncovered |
| SC-008 | --help exits 0 on all subcommands           | —                | Uncovered |
