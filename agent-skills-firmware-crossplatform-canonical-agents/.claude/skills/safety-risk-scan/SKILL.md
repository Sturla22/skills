---
name: safety-risk-scan
description: Enumerate likely failure modes and required mitigations for safety- or reliability-sensitive changes. Use when reviewing a safety-sensitive change, auditing reliability, checking for failure modes, or performing a pre-merge safety review.
---

# Safety Risk Scan

## Goal
Surface hazardous or reliability-critical failure modes early.

## Use when
- changing storage, control logic, sensor handling, transport, or state machines
- behavior on timeout, reboot, or bad input matters
- the code is safety- or reliability-sensitive

## Process
1. Read the changed code and identify all failure-relevant paths.
   ```
   grep -rn "timeout\|reboot\|watchdog\|assert\|overflow\|corrupt" src/
   ```
2. Check for each failure mode:
   - stale or missing data
   - timeout and retry behavior
   - reboot or power-loss mid-operation
   - partial writes or torn state
   - invalid inputs or corrupt payloads
   - queue saturation or dropped events
   - watchdog interactions
   - silent failure or misleading status
3. Assess: is each failure mode mitigated, accepted, or unknown?
4. Produce the risk summary.

## Guardrails
- Do not approve safety-sensitive changes without this scan — even if tests pass.
- "It hasn't happened yet" is not a mitigation — assess the theoretical failure path.
- Every identified gap must have a named owner and resolution path before merge.
- Silent failures are never acceptable in safety-sensitive paths — require a diagnostic signal.

## Failure Classification
- **Unmitigated gap**: a failure mode has no mitigation and no accepted-risk decision — block merge until resolved.
- **Missing test**: a failure mode is identified but has no corresponding test — add a fault injection test.
- **Misclassified severity**: a failure mode was listed as low-risk but has safety-critical consequences — re-escalate.

## Output Contract
- failure modes enumerated
- consequences stated
- mitigations or gaps listed
- required tests
