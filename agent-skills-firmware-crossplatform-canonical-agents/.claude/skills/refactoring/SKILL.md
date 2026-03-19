---
name: refactoring
description: Improve internal structure while preserving externally visible behavior.
allowed-tools: Read, Grep, Glob, Bash
---


# Refactoring

## Goal
Improve structure without changing externally visible behavior.

## Use when
- duplication is causing pain
- boundaries or names are misleading
- the design is harder to follow than necessary

## Process
1. State the behavior that must not change.
2. Add characterization tests if needed.
3. Pick one structural problem.
4. Change structure in small steps.
5. Run focused tests after each step.

## Done-when
- behavior is preserved
- structure is materially easier to understand

## Output
- preserved behavior
- structural problem addressed
- refactoring steps
- verification summary
