---
name: simulation-harness-first
description: Bias toward deterministic host-side simulation and fake time / I/O before hardware-only iteration.
allowed-tools: Read, Grep, Glob, Bash
---


# Simulation Harness First

## Goal
Create a fast, deterministic feedback loop for behavior that does not truly require target hardware.

## Use when
- debugging is slow on hardware
- logic mixes hardware interaction and decision-making
- you need characterization before refactor

## Process
1. Separate simulatable logic from target-only behavior.
2. Introduce fake time, fake I/O, fake storage, or fake transport as needed.
3. Capture the current behavior with deterministic fixtures.
4. Use the harness to drive debugging and TDD.

## Done-when
- the core behavior can be exercised without target hardware
- deterministic repros exist for the relevant scenarios

## Output
- what is simulated
- seams introduced
- fixtures used
- behaviors covered
