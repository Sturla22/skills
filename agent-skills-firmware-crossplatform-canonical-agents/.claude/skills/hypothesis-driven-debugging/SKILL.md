---
name: hypothesis-driven-debugging
description: Debug by ranking concrete hypotheses and running discriminating checks. Use when debugging a hard-to-find bug, diagnosing an unclear symptom, performing root cause analysis, or avoiding broad trial-and-error edits.
---

# Hypothesis-Driven Debugging

## Goal
Find root cause through evidence, not broad trial-and-error edits.

## Use when
- the symptom is real but the cause is unclear
- many plausible failure points exist
- logs are noisy or misleading

## Process
1. Read the relevant code and logs to define the symptom precisely.
   ```
   grep -rn "ERROR\|WARN\|assert\|panic" logs/ src/
   ```
2. Tighten the repro if possible.
3. List plausible hypotheses.
4. Rank them by likelihood and testability.
5. Design the cheapest discriminating check.
6. Run the check and update beliefs.
7. Repeat until root cause is supported.

## Guardrails
- Do not make code changes to test a hypothesis — use reads, logs, and targeted checks only.
- A hypothesis must be falsifiable — if it cannot be disproved, it is speculation.
- Do not fix symptoms — confirm root cause before writing any fix.
- Keep a written list of hypotheses and evidence — debugging from memory loses information.

## Failure Classification
- **Unfalsifiable hypothesis**: the check can't distinguish the hypothesis from alternatives — redesign the check.
- **Hypothesis loop**: evidence keeps pointing back to the same inconclusive area — the root cause is probably one layer deeper.
- **Repro lost**: the symptom disappeared — do not ship without understanding why; the bug is dormant.

## Output Contract
- symptom defined precisely
- hypotheses considered
- evidence for and against each
- root cause identified
- fix summary
- verification summary
