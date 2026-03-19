---
name: hardware-abstraction
description: Keep direct hardware access behind a narrow seam and separate policy from mechanism.
---


# Hardware Abstraction

## Goal
Prevent hardware-specific details from leaking into higher-level logic.

## Use when
- application code talks directly to peripherals
- platform migration is underway
- host simulation is difficult because the seam is missing

## Process
1. Identify direct hardware touch points.
2. Define a narrow capability-oriented boundary.
3. Move policy and decision logic above the boundary.
4. Keep vendor and board details below the boundary.
5. Create a fake or simulation seam if practical.

## Done-when
- hardware touches are localized
- the boundary is explicit
- higher-level logic is easier to test on host

## Output
- touch points found
- abstraction boundary
- responsibilities above vs below
- test seam
