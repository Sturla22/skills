---
name: tdd
description: Drive implementation with a failing test, the smallest passing change, and safe cleanup.
allowed-tools: Read, Grep, Glob, Bash
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
1. Express one behavior as the smallest failing test.
2. Confirm failure for the expected reason.
3. Make the smallest change that passes.
4. Run focused tests.
5. Refactor only while tests stay green.

## Done-when
- desired behavior is covered
- failure was observed before the fix
- relevant tests pass

## Output
- failing behavior pinned down
- tests added or changed
- implementation summary
- proof that tests pass
