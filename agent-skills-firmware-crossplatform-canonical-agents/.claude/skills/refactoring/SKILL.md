---
name: refactoring
description: Improve internal structure while preserving externally visible behavior. Use when cleaning up code structure, removing duplication, improving names or boundaries, or restructuring a module without changing its observable behavior.
---

# Refactoring

## Goal
Improve structure without changing externally visible behavior.

## Use when
- duplication is causing pain
- boundaries or names are misleading
- the design is harder to follow than necessary

## Process
1. Read the target area and state the behavior that must not change.
   ```
   grep -rn "TargetFunction\|TargetModule" src/ tests/
   ```
2. Add characterization tests if needed to pin current behavior.
3. Pick one structural problem.
4. Change structure in small steps.
5. Run focused tests after each step.
   ```
   make test
   ```

## Guardrails
- Never refactor and add behavior in the same commit — separate the concerns.
- Characterization tests must exist before any structural change.
- Change one structural problem per step — do not bundle multiple refactors.
- Do not rename public symbols without updating all callers in the same change.

## Failure Classification
- **Behavior regression**: tests fail after a structural change — revert the last step and isolate.
- **Missing characterization**: no tests cover the changed behavior — add coverage before proceeding.
- **Creeping scope**: the refactor is growing to touch unrelated areas — stop and scope it down.

## Output Contract
- preserved behavior stated
- structural problem addressed
- refactoring steps taken
- verification summary
