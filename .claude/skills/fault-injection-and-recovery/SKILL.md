---
name: fault-injection-and-recovery
description: Exercise timeout, corruption, missing-device, reset, and other failure scenarios deliberately. Use when testing error paths, verifying recovery behavior, checking fault tolerance, stress-testing failure handling, or confirming safe degradation under faults.
allowed-tools: Read, Grep, Glob, Bash
---

# Fault Injection and Recovery

Verify failure handling deliberately instead of assuming it is correct.

## Process

1. **Identify fault injection points** — find error-handling paths and recovery logic relevant to the change.
   ```
   Grep("error|fail|timeout|retry|recover|watchdog|reset", type="<lang>")
   ```

2. **Define the steady state** — before injecting anything, establish a measurable "healthy" baseline (correct output, expected log, heartbeat cadence). This is the target to return to.

3. **Select scenarios** — choose from the taxonomy below based on what the change touches.

4. **Inject each fault** — trigger via test hook, mock return value, or deliberate bad input; observe behavior.

5. **Assert recovery** — classify the outcome and verify the system reaches the expected state within a defined time bound:
   - **Benign** — fault masked or corrected; no observable effect. ✓ Best case.
   - **Graceful degradation** — reduced but correct and safe behavior continues. ✓ Acceptable.
   - **Safe-state entry** — outputs halted, human/supervisory intervention required. ✓ Acceptable for safety-critical.
   - **Crash/reset** — system resets; verify it is clean and logged. △ Detectable, may be recoverable.
   - **Silent Data Corruption (SDC)** — system runs but output is wrong with no error flagged. ✗ Worst case — most dangerous, hardest to detect.

6. **Document gaps** — list scenarios that could not be injected and why.

## Scenarios taxonomy
- timeout / deadline miss
- missing, late, or unreachable dependency
- corrupt or truncated input (CRC failure, framing error)
- reset or power loss mid-operation (interrupted NVM write, partial flash update)
- partial write / torn state
- queue saturation / dropped events
- repeated retry exhaustion
- watchdog starvation (code hangs but timer interrupt still fires)
- stack overflow (write past canary)
- invalid inputs / out-of-range sensor values

## Watchdog-specific patterns to test
- **"Kick on timer" anti-pattern** — deadlock the application while leaving the timer alive; watchdog must still fire.
- **Missing escalation** — inject a fault that survives resets; verify N consecutive resets triggers safe-mode or NVM-logged escalation, not an infinite reset loop.
- **Conditional feeding** — watchdog must only be kicked when application-level health checks pass, not on a bare timer.

## Guardrails
- Never inject faults into production systems — use test harnesses, fakes, or simulation.
- Do not mark a scenario "tested" unless it was actually exercised, not just reasoned about.
- SDC is the highest-severity outcome — design and test explicitly to minimize SDC rate.
- Log fault context to NVM before any reset; boot-reason register must show the expected reset cause.

## When injection is blocked
- **No test seam** — note as gap; recommend adding a seam (interface, hook, or flag) before next iteration.
- **Fault causes undefined behavior** — stop; flag as safety concern requiring architectural fix.
- **Recovery is hardware-dependent** — document expected behavior; test via simulation harness where available.

## Done-when
- the relevant failure scenarios were exercised or explicitly assessed
- expected safe behavior is defined
- recovery gaps are visible

## Output
- steady-state baseline
- scenarios tested (with outcome classification)
- observed recovery behavior
- gaps (with reason)
- follow-up work
