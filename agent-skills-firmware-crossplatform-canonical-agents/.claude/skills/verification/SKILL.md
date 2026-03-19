---
name: verification
description: Prove that the claimed change works and state clearly what remains unverified. Use when verifying a fix, checking a refactor, running regression tests, confirming a change works, or producing an evidence-based verdict before merge.
---

# Verification

## Goal
Demonstrate the main claim and relevant regressions as far as practical.

## Use when
- a code change was made
- a bug fix is claimed
- a refactor or migration needs evidence

## Process
1. Read the change and restate the claim being verified.
   ```
   grep -rn "changed_symbol\|changed_function" src/ tests/
   ```
2. Choose the strongest available checks.
3. Run focused checks first.
   ```
   make test
   ```
4. Run broader regression checks as needed.
5. Compare results to acceptance criteria.
6. State residual risk and unverified areas.

## Guardrails
- Do not declare verification passed if any regression failure remains.
- Every claim must map to a runnable check — verbal assertions are not verification.
- State what was NOT verified — partial verification presented as complete is a risk.
- Environment blockers (missing display, device, hardware) must be reported explicitly, not silently skipped.

## Failure Classification
- **Logic regression**: tests fail due to a real behavior change — must be fixed before claiming success.
- **Environment blocker**: test fails due to missing display, hardware, or toolchain — report as blocked, not as regression.
- **Missing coverage**: the claim cannot be verified because no test covers it — add the test or flag the gap.

## Output Contract
- claim verified
- checks run and results
- residual risk
- not verified (explicit list)
- verdict
