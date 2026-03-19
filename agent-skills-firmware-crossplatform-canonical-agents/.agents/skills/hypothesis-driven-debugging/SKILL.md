---
name: hypothesis-driven-debugging
description: Debug by ranking concrete hypotheses and running discriminating checks.
---


# Hypothesis-Driven Debugging

## Goal
Find root cause through evidence, not broad trial-and-error edits.

## Use when
- the symptom is real but the cause is unclear
- many plausible failure points exist
- logs are noisy or misleading

## Process
1. Define the symptom precisely.
2. Tighten the repro if possible.
3. List plausible hypotheses.
4. Rank them by likelihood and testability.
5. Design the cheapest discriminating check.
6. Run the check and update beliefs.
7. Repeat until root cause is supported.

## Done-when
- root cause is stated clearly
- evidence supports the diagnosis
- the fix addresses that cause

## Output
- symptom
- hypotheses considered
- evidence for and against
- root cause
- fix summary
- verification summary
