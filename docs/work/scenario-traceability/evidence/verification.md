# Verification Record

- Work ID: `scenario-traceability`
- Date: 2026-03-20
- Verifier: developer (static trace; Bash not available — script traced by hand)

## Method

Script logic traced manually against each fixture. Two bugs found and fixed
before recording results (see notes). Fixture runs are deterministic given the
fixed file contents.

## Fixture trace results

### `all-covered/` — expected exit 0

`collect_scenario_ids`:
- `docs/scenarios.md` → SC-001, SC-002 (in body + trace table; distinct key per ID)
- `docs/work/feat-a/scenarios.md` → SC-001 (independent scope)
- `scenario_ids = {SC-001, SC-002}`

`collect_covered_ids (tests/**/*`)`:
- `tests/test_main.c` → `// Covers: SC-001`, `// Covers: SC-002` → both matched
- `tests/test_feature.py` → `# Covers: SC-001` → matched
- `covered_ids = {SC-001, SC-002}`

`uncovered = []`, `orphaned = []` → **exit 0 ✓**

### `gap/` — expected exit 1, names SC-003

`collect_scenario_ids`:
- `docs/scenarios.md` → SC-001, SC-002, SC-003
- `docs/work` does not exist → guard prevents OSError
- `scenario_ids = {SC-001, SC-002, SC-003}`

`collect_covered_ids`:
- `tests/test_main.c` → `// Covers: SC-001`, `// Covers: SC-002`
- "SC-003 is not yet covered" line has no `Covers:` prefix → SC-003 not matched
- `covered_ids = {SC-001, SC-002}`

`uncovered = [SC-003]` → **exit 1, SC-003 named ✓**

### `orphan/` — expected exit 1, names SC-999

`collect_scenario_ids`:
- `docs/scenarios.md` → SC-001
- `scenario_ids = {SC-001}`

`collect_covered_ids`:
- `tests/test_main.c` → `// Covers: SC-001` → matched
- `tests/test_main.c` → `// Covers: SC-999` → matched
- `covered_ids = {SC-001, SC-999}`

`uncovered = []`, `orphaned = [SC-999]` → **exit 1, SC-999 named ✓**

## Bugs found and fixed during trace

| # | Bug | Fix |
|---|-----|-----|
| 1 | `collect_scenario_ids` called `.glob()` on `docs/work` without checking existence → `OSError` on Python 3.12+ | Added `if work_dir.is_dir():` guard |
| 2 | `text.find("\n", match.end())` returns -1 on last line without trailing newline → wrong slice | `line_end == -1` now takes `text[line_start:]` |

## Acceptance criteria mapping

| AC | Criterion | Evidence | Pass? |
|----|-----------|----------|-------|
| SC-001 | Scenarios file readable plain English, unique SC-NNN IDs | `templates/scenarios-template.md` + fixture files | ✓ |
| SC-002 | `Covers: SC-NNN` in test file recognized by script | `all-covered/` trace — SC-001 and SC-002 matched | ✓ |
| SC-003 | Uncovered scenario → exit 1 + named | `gap/` trace — SC-003 named, exit 1 | ✓ |
| SC-004 | All covered → exit 0 | `all-covered/` trace — exit 0 | ✓ |
| SC-005 | Orphaned reference → exit 1 + named | `orphan/` trace — SC-999 named, exit 1 | ✓ |
| SC-006 | Auto-discovers both `docs/scenarios.md` and `docs/work/*/scenarios.md` | `all-covered/` trace — both files scanned | ✓ |
| SC-007 | Template + rule file self-contained | `templates/scenarios-template.md` + `.agents/rules/scenario-traceability.md` reviewed | ✓ |
| SC-008 | Trace table format is GFM, maps SC-NNN → test file(s) | All fixture scenario files contain GFM trace tables | ✓ |

## Residual risk

- Static trace only — no live script execution. A mechanical run is strongly
  recommended before release, specifically to confirm `pathlib.Path.glob()`
  behaviour on the host Python version.
- The regex `SC-\d+` picks up IDs in trace table rows as well as scenario text.
  This is harmless for correctness (IDs are still registered) but means
  `scenario_ids` file-path lists may contain duplicates. Cosmetic only.
- Script does not handle encoding errors in binary files gracefully beyond
  `errors="ignore"` — acceptable for a developer tool.
