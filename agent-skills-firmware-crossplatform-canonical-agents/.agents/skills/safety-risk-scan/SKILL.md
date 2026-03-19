---
name: safety-risk-scan
description: Enumerate likely failure modes and required mitigations for safety- or reliability-sensitive changes.
allowed-tools: Read, Grep, Glob, Bash
---


# Safety Risk Scan

## Goal
Surface hazardous or reliability-critical failure modes early.

## Use when
- changing storage, control logic, sensor handling, transport, or state machines
- behavior on timeout, reboot, or bad input matters
- the code is safety- or reliability-sensitive

## Check for
- stale or missing data
- timeout and retry behavior
- reboot or power-loss mid-operation
- partial writes or torn state
- invalid inputs or corrupt payloads
- queue saturation or dropped events
- watchdog interactions
- silent failure or misleading status

## Done-when
- meaningful failure modes are listed
- mitigations or gaps are identified
- verification implications are clear

## Output
- failure modes
- consequences
- mitigations
- remaining gaps
- required tests
