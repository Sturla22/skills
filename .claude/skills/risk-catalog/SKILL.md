---
name: risk-catalog
description: Maintain a project-level risk catalog at docs/risks.md with stable RK-NNN
  IDs, FMEA fields, requirements linkage, and mechanical mitigation coverage checking
  via check-risks. Use when safety-risk-scan produces findings worth tracking permanently,
  when requirements carry failure-mode implications, or when verifying that cataloged
  risks have test-proven mitigations.
allowed-tools: Read, Grep, Glob, Bash
---

# Risk Catalog

Maintain a persistent, project-level list of failure modes and their test-proven
mitigations. Stable `RK-NNN` IDs survive across work packets and releases.

## When to use

- After `safety-risk-scan` produces findings with S ≥ 8 or systemic scope: promote
  them into the catalog so they outlive the work packet
- When writing requirements that carry failure-mode implications: link the risk
  before behavioral tests are written
- During review or release readiness: run `check-risks` to confirm no cataloged
  risk is unmitigated

## Catalog location

| Scope | Path |
|---|---|
| Project-wide (only) | `docs/risks.md` |

Use `templates/risk-catalog-template.md`. Risk IDs are project-scoped; there is no
per-work-packet risk file. Per-work-packet FMEA analysis lives in
`docs/work/<work-id>/evidence/` and feeds the catalog; it does not replace it.

## ID format

- Pattern: `RK-NNN` — three-digit minimum, zero-padded (e.g. `RK-001`, `RK-042`)
- Assign the next available integer on creation
- Never renumber existing IDs — stability matters for audit and traceability
- Retire a risk by setting Status to `Retired` and noting the reason; do not delete

## Relation to safety-risk-scan

`safety-risk-scan` is the discovery tool: use it during a work packet to enumerate
failure modes for the change at hand. When a finding meets any of these criteria,
promote it to `docs/risks.md` with a new `RK-NNN` ID:

- Severity S ≥ 8
- The failure mode is systemic (affects multiple work packets or subsystems)
- No concrete mitigation is assigned within this work packet

The scan output is the analysis; the catalog is the durable record.

## Test annotation syntax

Add a comment in each mitigating test. `Mitigates:` followed by the ID is the
machine-parseable signal:

```c
/* Mitigates: RK-003 */
```
```python
# Mitigates: RK-003
```

A single test may mitigate multiple risks (one `Mitigates:` line per ID).
A single risk may be covered by multiple tests.

## Coverage script

```sh
python scripts/cli.py check-risks
python scripts/cli.py check-risks --root <dir>
python scripts/cli.py check-risks --tests "src/tests/**/*"
```

Exit 0 — all cataloged risks have at least one `Mitigates:` test annotation,
no orphaned references.
Exit 1 — one or more risks unmitigated, or a test references an undefined `RK-NNN`.

## Process

1. After `safety-risk-scan`, identify findings that meet the promotion criteria above
2. Add a `## RK-NNN — <short title>` section to `docs/risks.md`; fill all FMEA fields
3. Populate "Requirements threatened" with the relevant requirement or scenario IDs
4. Write or update mitigating tests; add `Mitigates: RK-NNN` to each
5. Run `python scripts/cli.py check-risks` — resolve all gaps before closing the work

## Guardrails

- Do not add an entry without filling S, O, D, and RPN
- Do not mark Status as "Mitigated" without at least one `Mitigates:` test annotation
- Do not delete `RK-NNN` IDs — retire them instead; deletion breaks audit trails
- Safety-critical risks (S ≥ 8) that remain Open block release readiness

## Done-when

- All promoted FMEA findings have `RK-NNN` IDs in `docs/risks.md`
- Requirements linkages are filled for each entry
- Every non-retired cataloged risk has at least one `Mitigates:` test annotation
- `python scripts/cli.py check-risks` exits 0

## Output

- new or updated `RK-NNN` entries in `docs/risks.md`
- `Mitigates: RK-NNN` annotations added to mitigating tests
- `check-risks` exit 0 confirmation

## Relation to other skills

- `safety-risk-scan` — discover failure modes per work packet; hand high-severity or
  systemic findings here for permanent ID assignment
- `requirements-and-traceability` — use for forward linkage from risk through
  requirement to design and verification; risk-catalog is the failure-mode layer
- `scenario-traceability` — plain-English behavior coverage (SC-NNN → tests);
  risk-catalog is the failure-mode layer below that
- `release-readiness` — check that all Open, high-severity catalog entries are
  resolved before go/no-go
