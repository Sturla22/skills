---
name: fault-injection-and-recovery
description: Exercise timeout, corruption, missing-device, reset, and other failure scenarios deliberately.
---


# Fault Injection and Recovery

## Goal
Verify failure handling deliberately instead of assuming it is correct.

## Use when
- the change affects recovery paths
- safety or reliability matters
- bench testing mostly covers happy paths

## Scenarios to consider
- timeout
- missing or late dependency
- corrupt or truncated input
- reset or reboot mid-flow
- partial write
- queue overflow
- repeated retry exhaustion

## Done-when
- the relevant failure scenarios were exercised or at least explicitly assessed
- expected safe behavior is defined
- recovery gaps are visible

## Output
- scenarios tested
- observed recovery behavior
- gaps
- follow-up work
