---
name: fault-injection-and-recovery
description: Exercise timeout, corruption, missing-device, reset, and other failure scenarios deliberately. Use when testing error handling, validating fault recovery, checking timeout behavior, testing negative scenarios, or verifying that failure paths are safe.
---

# Fault Injection and Recovery

## Goal
Verify failure handling deliberately instead of assuming it is correct.

## Use when
- the change affects recovery paths
- safety or reliability matters
- bench testing mostly covers happy paths

## Process
1. Read the recovery paths and error handling in the target module.
   ```
   grep -rn "timeout\|retry\|error\|fail\|recover\|reset" src/
   ```
2. For each scenario below, assess: is it reachable? Is the expected safe behavior defined?
   - timeout
   - missing or late dependency
   - corrupt or truncated input
   - reset or reboot mid-flow
   - partial write
   - queue overflow
   - repeated retry exhaustion
3. Inject the fault in the test harness and observe behavior.
4. Record observed recovery behavior and gaps.

## Guardrails
- Do not inject faults directly into production code paths — use the test seam or fake layer.
- Every fault scenario must have an explicitly defined expected behavior before testing it.
- Do not claim "recovery is correct" based on happy-path tests alone.
- Fault injection tests must be deterministic — flaky fault tests are worse than no tests.

## Failure Classification
- **Silent failure**: the system fails the fault injection silently with no log or counter — add a diagnostic signal.
- **Non-deterministic recovery**: recovery behavior differs between runs — find the race or timing dependency.
- **Missing seam**: faults cannot be injected without modifying production code — introduce an injection point.

## Output Contract
- scenarios tested
- observed recovery behavior
- gaps identified
- follow-up work
