---
name: resource-budget-review
description: Review RAM, flash, stack, CPU, latency, and logging impact as part of the change. Use when reviewing resource usage, checking memory impact after a change, auditing a PR for resource regressions, or verifying a feature fits the resource budget.
---

# Resource Budget Review

## Goal
Treat resource use as part of correctness.

## Use when
- changing allocation patterns, buffers, queues, logs, timers, or state machines
- adding platform features or diagnostics
- moving behavior into a tighter execution context

## Process
1. Read the relevant code and identify resource touch points.
   ```
   grep -rn "malloc\|static\|stack\|buffer\|queue\|__attribute__" src/
   ```
2. Measure current resource use as a baseline.
   ```
   size build/firmware.elf
   ```
3. Apply the change and measure the delta.
4. Review: stack growth, RAM and flash impact, CPU cost and jitter, blocking time and latency, logging overhead, battery or power implications where relevant.

## Guardrails
- Always measure before and after — estimates without measurement are not sufficient for sign-off.
- Stack usage must be analyzed statically or measured under worst-case call depth.
- Do not approve a change that pushes a resource over 80% of budget without an explicit waiver.
- Logging overhead counts against the resource budget — especially on constrained targets.

## Failure Classification
- **Budget exceeded**: the change pushes a resource past the defined limit — scope down or optimize before merging.
- **Unmeasurable impact**: the toolchain cannot produce reliable numbers — flag and escalate before proceeding.
- **Unknown allocation**: heap or stack growth is non-deterministic — identify and bound the source.

## Output Contract
- resource areas touched
- expected impact with baseline and delta
- measurements or estimates
- unknowns
- follow-up checks
