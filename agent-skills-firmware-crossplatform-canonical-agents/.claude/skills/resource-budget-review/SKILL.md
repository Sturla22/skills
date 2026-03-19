---
name: resource-budget-review
description: Review RAM, flash, stack, CPU, latency, and logging impact as part of the change.
allowed-tools: Read, Grep, Glob, Bash
---


# Resource Budget Review

## Goal
Treat resource use as part of correctness.

## Use when
- changing allocation patterns, buffers, queues, logs, timers, or state machines
- adding platform features or diagnostics
- moving behavior into a tighter execution context

## Review
- stack growth
- RAM and flash impact
- CPU cost and jitter
- blocking time and latency
- logging overhead
- battery or power implications where relevant

## Done-when
- likely resource impacts are stated
- measurements or estimates are recorded
- hotspots or unknowns are visible

## Output
- resource areas touched
- expected impact
- measurements or estimates
- unknowns
- follow-up checks
