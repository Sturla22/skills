---
name: hardware-abstraction
description: Keep direct hardware access behind a narrow seam and separate policy from mechanism. Use when application code talks directly to peripherals, creating a platform abstraction layer, abstracting a driver, or making code testable on host without hardware.
---

# Hardware Abstraction

## Goal
Prevent hardware-specific details from leaking into higher-level logic.

## Use when
- application code talks directly to peripherals
- platform migration is underway
- host simulation is difficult because the seam is missing

## Process
1. Read the target module and identify all direct hardware touch points.
   ```
   grep -rn "HAL_\|register\|volatile\|mmio" src/
   ```
2. Define a narrow capability-oriented boundary.
3. Move policy and decision logic above the boundary.
4. Keep vendor and board details below the boundary.
5. Create a fake or simulation seam if practical.

## Guardrails
- The abstraction boundary must be a C function or type boundary — not a comment or convention.
- Do not put timing logic or retry policies inside the HAL — those belong above the seam.
- Keep the fake/simulation seam API-identical to the real HAL — no conditional compilation in callers.
- One peripheral or capability per abstraction unit — do not bundle unrelated hardware behind one interface.

## Failure Classification
- **Leaky abstraction**: hardware-specific types or constants appear above the seam — push them down.
- **Fat interface**: the boundary has more entry points than callers use — narrow it to the minimum needed.
- **Untestable seam**: the fake cannot be substituted at compile time — the seam design needs revision.

## Output Contract
- touch points found
- abstraction boundary defined
- responsibilities above vs below
- test seam described
