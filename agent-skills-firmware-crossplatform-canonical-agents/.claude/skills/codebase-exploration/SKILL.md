---
name: codebase-exploration
description: Map the relevant files, entry points, boundaries, and invariants before changing code. Use when entering an unfamiliar area, understanding code ownership, finding entry points, mapping data flow, or locating tests and seams before a change.
---

# Codebase Exploration

## Goal
Understand the minimum relevant slice of the codebase before acting.

## Use when
- entering an unfamiliar area
- ownership is unclear
- multiple modules may be involved
- tests and seams need to be found

## Process
1. Identify likely entry points from file names and top-level structure.
   ```
   grep -rn "main\|init\|register\|handler" src/
   ```
2. Read the key files to map relevant modules and boundaries.
3. Trace data flow and control flow through the relevant path.
4. Note key abstractions, invariants, and seams.
5. Locate tests and existing verification points.

## Guardrails
- Stop when the relevant slice is understood — do not read the whole codebase.
- Do not modify any files during exploration — changes come after this step.
- If ownership is genuinely unclear, flag it explicitly rather than assuming.
- Record assumptions about invariants so they can be verified before changing code.

## Failure Classification
- **Too broad**: exploration is covering unrelated modules — narrow the search to the change boundary.
- **Missing seam**: no test or injection point found — flag this as a risk before proceeding.
- **Stale map**: the code has diverged from any existing documentation — note the discrepancy.

## Output Contract
- relevant files listed
- entry points identified
- flow summary
- invariants noted
- test locations
