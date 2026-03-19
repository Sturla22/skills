---
name: firmware-migration
description: Move from legacy platform structure to a target structure in small, verified, reversible steps.
---


# Firmware Migration

## Goal
Migrate architecture or platform dependencies without betting the whole codebase at once.

## Use when
- moving to a new MCU, RTOS, transport, storage layer, or HAL structure
- replacing legacy platform glue
- splitting policy from platform code

## Process
1. Characterize the current externally visible behavior.
2. Define the target boundary.
3. Insert adapters or seams.
4. Migrate one path or responsibility at a time.
5. Keep rollback or coexistence options until confidence is high.
6. Remove legacy paths only after proof.

## Done-when
- migration steps are incremental
- behavior is preserved or intentionally changed with proof
- legacy compatibility debt is understood

## Output
- current behavior
- target boundary
- migration stages
- coexistence or rollback plan
- verification strategy
