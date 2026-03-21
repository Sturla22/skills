# Risk Catalog

## RK-001 — Watchdog not kicked under high load

**Status:** Mitigated
**Mitigating test(s):** tests/test_risks.c

## RK-002 — Stale sensor data silently used

**Status:** Mitigated
**Mitigating test(s):** tests/test_risks.c

## RK-003 — Power lost mid-write leaves NVM in torn state

**Status:** Open
**Severity (S):** 9
**Occurrence (O):** 4
**Detection difficulty (D):** 6
**RPN:** 216

**Failure mode:** Power failure interrupts a multi-byte NVM write; device boots with corrupt config.

**Mitigating test(s):**
<!-- No test yet — RK-003 is unmitigated -->
