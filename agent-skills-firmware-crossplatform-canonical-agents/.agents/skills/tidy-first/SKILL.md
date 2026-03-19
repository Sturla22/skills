---
name: tidy-first
description: Make tiny behavior-preserving cleanups that make the next change easier.
---


# Tidy First

## Goal
Reduce local friction before making the real change.

## Use when
- the target change is harder than it should be
- naming, movement, or extraction would simplify the next step

## Process
1. Identify the local obstacle.
2. Make one tiny behavior-preserving cleanup.
3. Verify nothing changed.
4. Stop when the next step becomes clear.

## Done-when
- the next change is easier
- the tidy diff is locally justified
- behavior is preserved

## Output
- obstacle identified
- tidy steps
- why they help
- verification performed
