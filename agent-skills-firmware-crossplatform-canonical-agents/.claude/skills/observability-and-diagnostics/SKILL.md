---
name: observability-and-diagnostics
description: Add or refine the minimal logs, counters, asserts, and traces needed to verify and support the system. Use when adding logging, improving diagnostics, making a silent bug visible, adding counters or assertions, or making a migration auditable.
---

# Observability and Diagnostics

## Goal
Make the system diagnosable without drowning it in noise.

## Use when
- a bug is hard to localize
- a migration needs confidence signals
- failures are silent or ambiguous

## Process
1. Read the relevant code path and identify where failures or state transitions are silent.
   ```
   grep -rn "LOG\|TRACE\|assert\|counter" src/
   ```
2. Apply diagnostics principles:
   - log at boundaries that matter
   - use counters for recurring events
   - assert violated internal invariants
   - do not spam hot paths or ISRs
   - include units and identifiers where useful
3. Add the minimum signals needed for the current debugging goal.
4. Verify signals appear under the expected conditions.

## Guardrails
- Do not add logging inside ISRs or tight loops — measure the cost first.
- Every log line must include enough context to be actionable — no bare "error" messages.
- Diagnostics that cannot be disabled in production need explicit approval.
- Do not add signals "just in case" — each signal must have a named consumer or verification use.

## Failure Classification
- **Hot path overhead**: diagnostics measurably slow the system — move to a post-processing or sampling approach.
- **Signal not reachable**: the added log never fires in testing — the instrumentation point is wrong.
- **Noise flood**: diagnostics obscure the failure instead of isolating it — reduce log verbosity, add filtering.

## Output Contract
- diagnostics added or proposed
- why each signal exists
- expected usage in verification
