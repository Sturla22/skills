---
name: verification
description: Prove that the claimed change works and state clearly what remains unverified.
allowed-tools: Read, Grep, Glob, Bash
---


# Verification

## Goal
Demonstrate the main claim and relevant regressions as far as practical.

## Use when
- a code change was made
- a bug fix is claimed
- a refactor or migration needs evidence

## Process
1. Restate the claim being verified.
2. Choose the strongest available checks.
3. Run focused checks first, then broader ones as needed.
4. Compare results to acceptance criteria.
5. State residual risk and unverified areas.

## Done-when
- the main claim is demonstrated
- relevant regressions were checked
- limitations are stated honestly

## Output
- claim verified
- checks run
- results
- residual risk
- not verified
- verdict
