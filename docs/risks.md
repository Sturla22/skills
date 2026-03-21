# Risk Catalog

<!-- PROJECT-LEVEL — lives at docs/risks.md                                    -->
<!-- HOW TO USE                                                                 -->
<!-- 1. Add one risk per ## section. Include FMEA fields and link requirements. -->
<!-- 2. Assign the next available RK-NNN ID. Never renumber existing entries.   -->
<!-- 3. In each mitigating test add a comment: Mitigates: RK-NNN               -->
<!-- 4. Run `python scripts/cli.py check-risks` to verify mitigation coverage.  -->
<!-- 5. Feed high-severity findings from safety-risk-scan into new entries here. -->

## RK-001 — Interrupted NVM write corrupts device state

**Category:** Data integrity
**Status:** Open
**Severity (S):** 9
**Occurrence (O):** 4
**Detection difficulty (D):** 6
**RPN:** 216

**Failure mode:** Power is lost during a multi-byte NVM write, leaving the record
partially written. On next boot the device reads corrupt data and may enter an
undefined state.

**Consequence:** Silent data corruption; device may operate on stale or invalid
configuration with no error flagged.

**Requirements threatened:**
<!-- Replace with real requirement or scenario IDs, e.g. REQ-042, SC-003 -->

**Mitigation:** Dual-bank write with atomic swap; write-verify step after every
commit; revert-to-default-on-invalid-signature boot path.

**Residual risk:** A simultaneous failure of both NVM banks is not covered by this
mitigation (extremely low probability; treat as safe-state entry condition).

**Mitigating test(s):**
<!-- Add Mitigates: RK-001 to each covering test, then run check-risks -->

---

<!-- Add new risks below. Use the next integer; do not reuse or renumber. -->

## Trace table

| ID | Short title | Category | RPN | Status | Requirements threatened | Mitigating test(s) |
|---|---|---|---|---|---|---|
| RK-001 | Interrupted NVM write corrupts device state | Data integrity | 216 | Open | | |
