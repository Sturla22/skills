---
paths:
  - "docs/scenarios.md"
  - "docs/work/*/scenarios.md"
  - "tests/**/*"
---

# Scenario Traceability

- Scenario files live at `docs/scenarios.md` (project-wide) and
  `docs/work/<work-id>/scenarios.md` (per feature). Use `docs/templates/scenarios-template.md`.
- Every scenario gets a unique `SC-NNN` ID (three-digit zero-padded). Never renumber existing IDs.
- Every covering test carries a comment `Covers: SC-NNN` — one line per scenario ID.
- Run `python tools/cli.py check-coverage` to verify all scenarios are covered.
  Exit 0 = fully covered; exit 1 = gap or orphaned reference.
- The trace table in the scenarios file is human-maintained and informational;
  the script is the authoritative source of coverage truth.
- See the `scenario-traceability` skill for full guidance.
