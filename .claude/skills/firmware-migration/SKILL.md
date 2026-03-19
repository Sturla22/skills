---
name: firmware-migration
description: Move from legacy platform structure to a target structure in small, verified, reversible steps. Use when migrating to a new MCU, RTOS, HAL, or transport layer, replacing legacy platform glue, splitting policy from platform code, or porting firmware to a new target.
allowed-tools: Read, Grep, Glob, Bash
---

# Firmware Migration

Migrate architecture or platform dependencies without betting the whole codebase at once.

## Process

1. **Characterize current behavior** — read the relevant modules; note the externally visible behavior that must be preserved or intentionally changed.
   ```
   Glob("**/*.{c,h,cpp,rs}"), Grep("<platform-symbol>|HAL_|vendor_")
   ```

2. **Define the target boundary** — state what the new structure looks like and where the seam sits. Apply the Strangler Fig pattern: wrap legacy subsystems behind a stable interface; replace implementations one at a time beneath it.

3. **Insert adapters or seams first** — add thin adapter layers between old and new without changing behavior yet. The adapter is the routing proxy; behavior above it is unaware of what changes below.

4. **Apply the phased bottom-up migration order:**
   - Startup code and linker script (clock init, vector table, memory regions)
   - GPIO and basic timers — proves toolchain works on the new target
   - Communication peripherals one at a time (UART, SPI, I2C)
   - RTOS kernel (if changing) — requires all drivers stable first
   - Application logic last

5. **Use CMSIS-RTOS2 as a migration buffer** (when changing RTOS) — write RTOS calls against the CMSIS-RTOS2 API; swap the kernel beneath without touching application code.

6. **Keep coexistence or rollback options** — old and new paths coexist until confidence is high:
   - *A/B flash partitions*: watchdog-guarded trial boot; rollback on failure.
   - *Shadow mode / dual-run*: both paths execute; compare output before promoting the new one.
   - *Compile-time feature flag*: `#ifdef NEW_HAL` for incremental driver swaps.
   - Ownership of each peripheral must be exclusive — never let both paths drive the same registers simultaneously.

7. **Verify each stage before proceeding** — run regression tests on host (hardware-stubbed) first, then on target. Do not migrate and refactor simultaneously.

8. **Remove legacy paths** — only after each migrated path is proven. Delete, don't comment out.

## Common cross-family failure modes to check
- **Endianness** — Cortex-M is always little-endian; RISC-V can be either; serialization code silently breaks.
- **Memory map** — peripheral base addresses, flash/RAM sizes, DMA alignment all change.
- **Clock tree** — the most common first-boot failure after a family change; bring up LED blink before anything else.
- **Compiler/ABI** — struct packing, calling conventions, and `volatile` semantics may differ between toolchains.

## Guardrails
- Never migrate more than one responsibility per step.
- Do not delete legacy code until the replacement is verified.
- Do not refactor and migrate simultaneously — tidy first, then migrate.
- Peripheral ownership must be exclusive during any coexistence period.

## When migration stalls
- **Seam cannot be inserted cleanly** — apply `tidy-first` or `hardware-abstraction` first.
- **Behavior cannot be characterized** — add observability or simulation harness before proceeding.
- **Hardware dependency blocks host testing** — use simulation harness to cover what is testable; flag the rest.

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
