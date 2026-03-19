---
name: observability-and-diagnostics
description: Add or refine the minimal logs, counters, asserts, and traces needed to verify and support the system.
---


# Observability and Diagnostics

## Goal
Make the system diagnosable without drowning it in noise.

## Use when
- a bug is hard to localize
- a migration needs confidence signals
- failures are silent or ambiguous

## Principles
- log at boundaries that matter
- use counters for recurring events
- assert violated internal invariants
- do not spam hot paths or ISRs
- include units and identifiers where useful

## Done-when
- important failure boundaries have signals
- diagnostics are cheap enough to keep
- verification can use the signals meaningfully

## Output
- diagnostics added or proposed
- why each signal exists
- expected usage in verification
