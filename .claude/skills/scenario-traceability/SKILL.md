---
name: scenario-traceability
description: Keep plain-English usage scenarios linked to tests with stable IDs and mechanical coverage checking. Use when starting a feature, writing acceptance criteria, or verifying that every stated user need has at least one covering test.
allowed-tools: Read, Grep, Glob, Bash
---

# Scenario Traceability

Maintain a living list of human-readable usage scenarios with stable `SC-NNN`
IDs. Link each scenario to the tests that cover it. Verify coverage mechanically.

## When to use

- At the start of a feature: create or update the scenarios file before writing tests
- During review: run the coverage script to confirm no scenario is orphaned
- During handoffs: the scenarios file is the plain-English record of intent

## Scenario file locations

| Scope | Path |
|---|---|
| Project-wide | `docs/scenarios.md` |
| Per feature / work packet | `docs/work/<work-id>/scenarios.md` |

Use `templates/scenarios-template.md` for both. IDs are independent per file;
the file path provides scope context.

## ID format

- Pattern: `SC-NNN` — three-digit minimum, zero-padded (e.g. `SC-001`, `SC-042`)
- Assign the next available integer on creation
- Never renumber existing IDs — stability matters for traceability
- Two files may independently have `SC-001`; they are distinct by file path

## Writing a scenario

Keep it in plain English. One sentence is enough. Write for a non-technical
reader. Do not describe implementation; describe what the user or system does
and what outcome they get.

```markdown
**SC-003** — When power is lost mid-write, the device detects the partial
record on next boot and recovers to the last valid state.
```

## Test reference syntax

Add a comment in the covering test. The keyword `Covers:` followed by the ID
is the machine-parseable signal. Language-appropriate comment style:

```c
// Covers: SC-003
```
```python
# Covers: SC-003
```
```cpp
// Covers: SC-003
```

A single test may cover multiple scenarios; use one `Covers:` line per ID.
A single scenario may be covered by multiple tests.

## Trace table

Keep a GFM table in the scenarios file mapping each ID to its covering test(s).
The table is informational; the script is the authoritative coverage check.

| ID     | Description (short)         | Covering test(s)           | Status  |
|--------|-----------------------------|----------------------------|---------|
| SC-001 | Sample rate validated        | tests/unit/test_config.c   | Covered |

## Coverage script

```sh
# Check coverage from repo root (auto-discovers both scope levels):
python scripts/cli.py check-coverage

# Check a specific subtree (e.g. a fixture):
python scripts/cli.py check-coverage --root <dir>

# Override test glob:
python scripts/cli.py check-coverage --tests "src/tests/**/*"

```

Exit 0 — all scenarios covered, no orphaned references.
Exit 1 — one or more scenarios uncovered, or a test references an undefined ID.

## Process

1. Create or update the scenarios file using `templates/scenarios-template.md`
2. Assign `SC-NNN` IDs to each scenario before writing tests
3. Write tests; add `Covers: SC-NNN` to each covering test
4. Update the trace table
5. Run `python scripts/cli.py check-coverage` — fix any gaps before closing

## Guardrails

- Do not renumber IDs; insert new ones at the end with the next integer
- Do not write scenarios in implementation terms (no function names, no variable names)
- Do not skip the coverage script before declaring a feature complete
- Do not let the trace table drift from reality — the script will catch it
- If a scenario cannot be covered by any automated test, say so explicitly and
  record why (hardware-only, manual-only, deferred)

## Done-when

- Scenarios file exists and is readable without tooling
- Every scenario has a unique `SC-NNN` ID
- Every test that covers a scenario carries a `Covers: SC-NNN` comment
- `python scripts/cli.py check-coverage` exits 0

## Relation to other skills

- Use `bdd` to discover and formulate the scenarios; hand stable scenarios here
  for ID assignment and traceability wiring
- Use `requirements-and-traceability` when you need formal linkage from
  stakeholder needs through requirements to design and verification evidence;
  scenario traceability is the lightweight layer that sits above test code
