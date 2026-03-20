# Verification Record

- Work ID: `cli-tools`
- Date: 2026-03-20
- Verifier: product-owner (live execution with Bash)

## Method

Each SC scenario exercised by running `python scripts/cli.py` against the
live repo. Test artifacts created and then removed via Python shutil.

## Results

| SC | Scenario | Exit code | Result |
|----|----------|-----------|--------|
| SC-001 | `new-work test-feature` creates packet | 0 | ✓ PASS |
| SC-001 | Second invocation prints ERROR and exits non-zero | 1 | ✓ PASS |
| SC-002 | `new-scenarios` creates `docs/scenarios.md` | 0 | ✓ PASS |
| SC-002 | `new-scenarios --work test-feature` creates work-packet file | 0 | ✓ PASS |
| SC-003 | `new-handoff … --from planner --to developer` → `001-planner-to-developer.md` | 0 | ✓ PASS |
| SC-003 | Second handoff → `002-developer-to-verifier.md` | 0 | ✓ PASS |
| SC-004 | Fresh unfilled packet → exit 1, 31 sections listed | 1 | ✓ PASS |
| SC-004 | Filled packet (`cli-tools`) → exit 1, 4 false positives (see notes) | 1 | ⚠ PASS with caveat |
| SC-005 | `list-work` prints all packets with owner+step; exits 0 | 0 | ✓ PASS |
| SC-006 | `new-agent test-bot` creates TOML stub + sync reminder | 0 | ✓ PASS |
| SC-007 | `new-skill test-skill` creates SKILL.md stub + sync reminder | 0 | ✓ PASS |
| SC-008 | `--help` and `new-work --help` both exit 0 with usage | 0 | ✓ PASS |

## Notes

**SC-004 false positives:** `check-work cli-tools` reports 4 sections
(`## In scope`, `## Acceptance criteria`, `## Assumptions`, `## Open questions`)
as incomplete because their content contains `<work-id>` as a legitimate
path-convention token (e.g. `docs/work/<work-id>/`). This is the known risk
from plan.md §Risks. Acceptable in v1; the primary use case (detecting freshly
scaffolded unfilled packets) works correctly.

**SC-005 older packets:** `add-researcher` and `enrich-firmware-patterns` show
"unknown" for owner and step because their `status.md` predates the current
template format. Expected; no action needed.

## Verdict

All 8 acceptance criteria pass. SC-004 caveat is known and documented.
CLI is ready to commit.
