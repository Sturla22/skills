# Risk Catalog

## RK-001 — Watchdog not kicked under high load

**Category:** Reliability
**Status:** Mitigated
**Severity (S):** 8
**Occurrence (O):** 3
**Detection difficulty (D):** 5
**RPN:** 120

**Failure mode:** CPU load exceeds budget; watchdog kick is delayed past the timeout window.

**Mitigation:** Challenge-response WDT with per-task health tokens.

**Mitigating test(s):** tests/test_risks.c

## RK-002 — Stale sensor data silently used

**Category:** Data integrity
**Status:** Mitigated
**Severity (S):** 7
**Occurrence (O):** 4
**Detection difficulty (D):** 6
**RPN:** 168

**Failure mode:** Sensor read fails; last-value-held is used without freshness check.

**Mitigation:** Freshness counter validated before every use; stale data triggers fault.

**Mitigating test(s):** tests/test_risks.c
