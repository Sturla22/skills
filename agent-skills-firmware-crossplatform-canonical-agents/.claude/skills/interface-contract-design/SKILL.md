---
name: interface-contract-design
description: Define stable module contracts with explicit inputs, outputs, failure modes, timing, and ownership. Use when designing a new API boundary, reviewing an interface for stability, establishing a HAL contract, or stabilizing a module before refactor or migration.
---

# Interface Contract Design

## Goal
Define a contract that can survive implementation changes and platform migration.

## Use when
- introducing or changing a boundary
- reshaping a HAL or service interface
- stabilizing a module before refactor or migration

## Process
1. Read the current interface and all its callers.
   ```
   grep -rn "FunctionName\|ModuleName" src/
   ```
2. Make explicit:
   - responsibilities and non-goals
   - inputs and outputs
   - units and ranges
   - ownership and lifetime
   - sync vs async behavior
   - ISR / thread / task context
   - error model and retry expectations
   - versioning or compatibility constraints
3. Draft the contract document or header comment.
4. Confirm callers and implementers agree on the same contract.

## Guardrails
- Do not define a contract for code you haven't read — always read callers and implementers first.
- Do not leave error model or ownership undefined — these are the most common sources of bugs.
- Do not mix policy decisions into the contract definition — keep mechanism separate.
- A contract change requires updating all callers before merging.

## Failure Classification
- **Ambiguous contract**: callers disagree on semantics — list the ambiguity explicitly and resolve it before finalizing.
- **Missing failure mode**: a reachable error path is not covered — add it to the error model.
- **Scope too wide**: the contract is trying to cover too many responsibilities — split the interface.

## Output Contract
- contract summary
- invariants
- failure modes
- compatibility notes
- verification implications
