---
name: simplify-without-behavior-change
description: Remove accidental complexity without changing externally visible behavior.
allowed-tools: Read, Grep, Glob, Bash
---


# Simplify Without Behavior Change

## Goal
Eliminate accidental complexity.

## Principles
- remove before add
- inline before abstract
- merge before split
- specialize before generalize

## Use when
- code feels overengineered
- wrappers add little value
- flags or state paths are tangled
- obsolete options or branches remain

## Process
1. State the behavior that must remain.
2. Identify accidental rather than essential complexity.
3. Add characterization tests if needed.
4. Remove one complexity source at a time.
5. Re-run tests after each simplification.

## Done-when
- same visible behavior
- fewer moving parts
- fewer special cases
- easier to explain

## Output
- preserved behavior
- accidental complexity found
- simplifications made
- items removed
- verification summary
