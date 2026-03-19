---
name: safety-risk-scan
description: Enumerate likely failure modes and required mitigations for safety- or reliability-sensitive changes. Use when changing storage, control logic, sensor handling, transport, or state machines, when behavior on timeout or reboot matters, or before merging safety-critical code.
allowed-tools: Read, Grep, Glob, Bash
---

# Safety Risk Scan

Surface hazardous or reliability-critical failure modes early.

## Process

1. **Read the change** — understand what paths are affected and what invariants they rely on.
   ```
   Grep("timeout|retry|watchdog|reset|power|write|state|interrupt", type="<lang>")
   ```

2. **Apply the FMEA approach** — for each affected function, ask "how can this fail?" using the standard taxonomy. Score each finding: **S**everity (1–10) × **O**ccurrence (1–10) × **D**etection difficulty (1–10) = RPN. Prioritize S ≥ 8 regardless of RPN.

3. **Apply HAZOP guide words to interfaces and data flows** — for each inter-module data flow or external interface:

   | Guide Word | Ask |
   |---|---|
   | NO / NOT | Signal absent when expected? |
   | MORE / LESS | Value out of expected range? |
   | EARLY / LATE | Timing violation? |
   | SPURIOUS | Action triggered without cause? |
   | PART OF | Incomplete execution or partial data? |
   | REVERSE | Inverted logic or polarity? |

4. **Check the failure checklist** — for each item, ask: "can this change cause this failure mode?"

5. **For each failure mode found** — state the consequence and the required mitigation. Mark items without a concrete mitigation as gaps blocking completion.

## Failure checklist
- stale or missing data (sensor last-value-held, freshness not checked)
- timeout and retry exhaustion
- reboot or power-loss mid-operation (interrupted NVM write, partial flash update)
- partial writes or torn state
- invalid inputs or corrupt payloads (no range/plausibility check)
- queue saturation or dropped events
- watchdog interactions (kick-on-timer anti-pattern; missing escalation after N resets)
- silent failure or misleading status (SDC — output wrong, no error flagged)
- race condition on shared ISR/task data
- stack overflow (especially in ISRs or new deep call chains)
- integer overflow / truncation (counter wraps, type truncation without assertion)

## Standard mitigations (reference)
| Failure Mode | Standard Mitigation |
|---|---|
| Watchdog not kicked | Challenge-response WDT; task-completion health tokens; never kick from interrupt |
| Interrupted NVM write | Dual-bank with atomic swap; write-verify; revert-on-invalid-signature boot |
| Stale sensor data | Freshness counter/timestamp on every reading; treat stale as invalid |
| Race condition on shared state | Critical section around shared variable; prefer queues over globals |
| Stack overflow | Static WCSA (`puncover`); canary guard regions; `uxTaskGetStackHighWaterMark` |
| Silent data corruption | CRC/checksum on critical structs; periodic flash CRC verification |

## Guardrails
- Do not mark a failure mode as "mitigated" without specifying the concrete mitigation.
- Do not skip checklist items — mark them "not applicable" with a reason.
- Safety-critical gaps block shipping — they do not get deferred to a follow-up.
- If a mitigation requires a separate task, create it explicitly rather than noting it informally.

## When scan is inconclusive
- **Behavior is hardware-dependent** — document assumed behavior; flag for hardware verification.
- **State machine is too complex** — apply `simulation-harness-first` to make it testable.
- **Multiple failure modes interact** — treat the interaction as a separate, higher-severity risk item.

## Done-when
- meaningful failure modes are listed with RPN scores
- mitigations or gaps are identified for each
- verification implications are clear

## Output
- failure modes (with S/O/D/RPN)
- consequences
- mitigations
- remaining gaps (blocking vs. non-blocking)
- required tests
