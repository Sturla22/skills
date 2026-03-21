---
paths:
  - "docs/risks.md"
  - "tests/**/*"
---

# Risk Catalog

- The project-level risk catalog lives at `docs/risks.md`. Use `docs/templates/risk-catalog-template.md`.
- Every risk gets a unique `RK-NNN` ID (three-digit zero-padded). Never renumber or delete existing IDs; retire them with Status: Retired.
- Every mitigating test carries a comment `Mitigates: RK-NNN` — one line per risk ID.
- Run `python tools/cli.py check-risks` to verify all cataloged risks have test-proven mitigations.
  Exit 0 = fully mitigated; exit 1 = gap or orphaned reference.
- Feed high-severity (S ≥ 8) or systemic findings from `safety-risk-scan` into the catalog.
- See the `risk-catalog` skill for full guidance.
