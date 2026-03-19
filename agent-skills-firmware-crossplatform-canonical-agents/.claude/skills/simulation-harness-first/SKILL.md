---
name: simulation-harness-first
description: Bias toward deterministic host-side simulation and fake time / I/O before hardware-only iteration. Use when setting up a test harness, making code testable on host, avoiding hardware dependency in tests, or creating fakes and stubs for peripherals.
---

# Simulation Harness First

## Goal
Create a fast, deterministic feedback loop for behavior that does not truly require target hardware.

## Use when
- debugging is slow on hardware
- logic mixes hardware interaction and decision-making
- you need characterization before refactor

## Process
1. Read the target module and identify the simulatable logic vs target-only behavior.
   ```
   grep -rn "HAL_\|CMSIS\|register\|volatile" src/
   ```
2. Introduce fake time, fake I/O, fake storage, or fake transport as needed.
3. Capture the current behavior with deterministic fixtures.
4. Build and run the harness on host.
   ```
   cmake -B build-host -DPLATFORM=host && cmake --build build-host && ./build-host/tests
   ```
5. Use the harness to drive debugging and TDD.

## Guardrails
- The host harness must use the same public API as the target — no test-only entry points in production code.
- Fake time must be injected at a single seam — not scattered through the logic.
- Do not skip the harness because "it's faster to test on hardware right now" — that debt compounds.
- The harness is not a replacement for on-target integration testing — it supplements it.

## Failure Classification
- **Tight coupling**: simulatable logic and hardware access are interleaved — extract the seam first.
- **Non-deterministic fixture**: the harness produces different results on repeated runs — find the hidden time or state dependency.
- **Host/target divergence**: harness passes but target fails — the fake is not faithful; tighten the abstraction.

## Output Contract
- what is simulated
- seams introduced
- fixtures used
- behaviors covered
