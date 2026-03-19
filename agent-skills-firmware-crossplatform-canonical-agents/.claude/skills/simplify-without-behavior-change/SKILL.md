---
name: simplify-without-behavior-change
description: Remove accidental complexity without changing externally visible behavior. Use when simplifying overengineered code, removing unnecessary abstractions, inlining a pointless wrapper, removing dead flags or branches, or reducing special cases.
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
1. Read the target area and state the behavior that must remain.
   ```
   grep -rn "flag\|option\|wrapper\|adapter" src/
   ```
2. Identify accidental rather than essential complexity.
3. Add characterization tests if needed.
4. Remove one complexity source at a time.
5. Re-run tests after each simplification.
   ```
   make test
   ```

## Guardrails
- Do not simplify and add behavior in the same change — one concern per commit.
- Remove dead code only after confirming it is truly unreachable (search all callers).
- Do not remove an abstraction that serves as a seam for testing — verify the test impact first.
- Simplification that breaks an external API requires a deprecation path, not a silent removal.

## Failure Classification
- **Behavior regression**: tests fail after simplification — revert and isolate the removal.
- **Hidden dependency**: the removed code was used by an obscure caller — search more broadly before removing.
- **Essential complexity removed**: the simplification broke a real requirement — restore it and reconsider.

## Output Contract
- preserved behavior stated
- accidental complexity found
- simplifications made
- items removed
- verification summary
