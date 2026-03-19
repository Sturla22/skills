---
name: tidy-first
description: Make tiny behavior-preserving cleanups that make the next change easier. Use when cleaning up before a feature, removing dead code, tidying naming, quick hygiene pass, or the target area is messy and needs low-risk prep first.
---

# Tidy First

## Goal
Reduce local friction before making the real change.

## Use when
- the target change is harder than it should be
- naming, movement, or extraction would simplify the next step
- dead code or duplication is obscuring intent

## Process
1. Read the target area to identify the obstacle.
   ```
   grep -rn "pattern" src/
   ```
2. Make one tiny behavior-preserving cleanup.
3. Verify nothing changed.
   ```
   make test
   ```
4. Stop when the next step becomes clear.

## Guardrails
- One tidy step at a time — do not bundle multiple cleanups into one diff.
- Do not rename public APIs without checking all callers first.
- Do not tidy and change behavior in the same commit.
- Tidy only what is needed for the next planned change — no speculative cleanup.

## Failure Classification
- **Behavior regression**: tests fail after tidy — revert the last step and isolate the change.
- **Scope creep**: tidy diff is growing beyond the obstacle — stop, commit what helps, defer the rest.
- **Unclear obstacle**: tidy doesn't make the next step easier — the real problem is a design issue, not a cleanup task.

## Output Contract
- obstacle identified
- tidy steps taken
- why they help
- verification performed
