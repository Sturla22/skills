---
name: interface-contract-design
description: Define stable module contracts with explicit inputs, outputs, failure modes, timing, and ownership.
allowed-tools: Read, Grep, Glob, Bash
---


# Interface Contract Design

## Goal
Define a contract that can survive implementation changes and platform migration.

## Use when
- introducing or changing a boundary
- reshaping a HAL or service interface
- stabilizing a module before refactor or migration

## Make explicit
- responsibilities and non-goals
- inputs and outputs
- units and ranges
- ownership and lifetime
- sync vs async behavior
- ISR / thread / task context
- error model and retry expectations
- versioning or compatibility constraints

## Done-when
- callers and implementers can agree on the same contract
- ambiguous behavior is removed
- verification expectations are clear

## Output
- contract summary
- invariants
- failure modes
- compatibility notes
- verification implications
