---
name: firmware-migration
description: Move from legacy platform structure to a target structure in small, verified, reversible steps. Use when migrating to a new MCU or RTOS, porting firmware to a new platform, replacing legacy HAL glue, or splitting policy from platform code incrementally.
---

# Firmware Migration

## Goal
Migrate architecture or platform dependencies without betting the whole codebase at once.

## Use when
- moving to a new MCU, RTOS, transport, storage layer, or HAL structure
- replacing legacy platform glue
- splitting policy from platform code

## Process
1. Read the current module and characterize its externally visible behavior.
   ```
   grep -rn "legacy_\|old_\|PLATFORM_\|BOARD_" src/
   ```
2. Define the target boundary.
3. Insert adapters or seams.
4. Migrate one path or responsibility at a time.
   ```
   make test
   ```
5. Keep rollback or coexistence options until confidence is high.
6. Remove legacy paths only after proof.

## Guardrails
- Never migrate more than one responsibility per step — batching migrations loses the safety net.
- Keep the legacy path buildable until the target path passes all tests.
- Do not remove legacy compatibility without an explicit sign-off from all dependents.
- Migration steps must be individually reversible — if a step cannot be reverted, split it further.

## Failure Classification
- **Behavior regression**: the migrated path fails tests the legacy path passed — revert the last step and isolate.
- **Coexistence conflict**: legacy and new paths interact unexpectedly — introduce a cleaner isolation seam.
- **Migration stall**: the adapter layer is becoming permanent — force a removal deadline or redesign the seam.

## Output Contract
- current behavior characterized
- target boundary defined
- migration stages listed
- coexistence or rollback plan
- verification strategy
