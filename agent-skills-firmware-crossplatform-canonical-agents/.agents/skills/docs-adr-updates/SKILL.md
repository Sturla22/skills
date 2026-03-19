---
name: docs-adr-updates
description: Keep README, architecture notes, and ADRs aligned with the implemented system.
---


# Docs and ADR Updates

## Goal
Keep written design truth aligned with code.

## Use when
- a design decision changed
- an interface or failure mode changed materially
- a migration path was introduced

## Process
1. Identify docs that are now stale.
2. Update the minimum set needed to restore alignment.
3. Record important tradeoffs and implications.
4. Note migration and rollback concerns.

## Done-when
- code and docs no longer contradict
- key decisions are recorded
- future readers can understand the intended design

## Output
- docs updated
- stale assumptions removed
- decisions recorded
- migration notes
