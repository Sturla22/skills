---
name: tdd
description: Drive implementation with a failing test, the smallest passing change, and safe cleanup. Use when implementing a new behavior test-first, reproducing a bug with a test, adding coverage, or applying red-green-refactor.
---

# TDD

## Goal
Use tests as the executable spec for the next small behavior change.

## Use when
- behavior can be expressed as a test
- a bug can be reproduced
- a feature needs a crisp spec
- a refactor needs a safety net

## Process
1. Read the existing tests and code for the target behavior.
   ```
   grep -rn "test_\|TEST_\|EXPECT\|ASSERT" tests/
   ```
2. Express one behavior as the smallest failing test.
3. Confirm failure for the expected reason.
   ```
   make test 2>&1 | grep -A5 "FAILED\|Error"
   ```
4. Make the smallest change that passes.
5. Run focused tests.
   ```
   make test
   ```
6. Refactor only while tests stay green.

## Guardrails
- Red before green — never write implementation before the failing test exists.
- One behavior per test — tests that cover multiple behaviors are harder to diagnose.
- Do not skip the refactor step — accumulating green debt is how TDD fails long-term.
- Test the behavior, not the implementation — avoid over-specifying internals.

## Failure Classification
- **Wrong failure reason**: test fails for a different reason than expected — fix the test before implementing.
- **Test passes immediately**: test was already green — the behavior was already implemented or the test is wrong.
- **Logic regression**: previously passing tests break — revert the last change and isolate.

## Output Contract
- failing behavior pinned down
- tests added or changed
- implementation summary
- proof that tests pass
