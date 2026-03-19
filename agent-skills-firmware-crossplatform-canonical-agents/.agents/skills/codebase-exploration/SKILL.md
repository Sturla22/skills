---
name: codebase-exploration
description: Map the relevant files, entry points, boundaries, and invariants before changing code.
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
1. Identify likely entry points.
2. Map relevant files and modules.
3. Trace data flow and control flow.
4. Note key abstractions, invariants, and seams.
5. Identify likely tests and verification points.

## Done-when
- relevant files are identified
- boundaries and flow are summarized
- likely change points are named

## Output
- relevant files
- entry points
- flow summary
- invariants
- test locations
