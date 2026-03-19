---
name: planning
description: Produce a concrete, staged plan with explicit verification before implementation. Use when planning before implementation, breaking down ambiguous work, structuring a multi-step approach, defining done criteria, or reducing risk before changing code.
---

# Planning

## Goal
Produce a low-risk, checkable plan.

## Use when
- the request is ambiguous
- multiple implementation options exist
- the work crosses modules or layers
- risk needs to be reduced before code changes

## Process
1. Read the relevant code, tests, and docs to understand current state before proposing anything.
   ```
   grep -rn "relevant_symbol\|TargetModule" src/ docs/
   ```
2. Restate the problem operationally.
3. Define the end state and non-goals.
4. Identify the smallest viable path.
5. Break the work into ordered steps.
6. Name assumptions and unknowns.
7. Define how success will be verified.

## Guardrails
- Do not propose a plan without first reading the relevant code — plans based on assumptions fail.
- Every step in the plan must be individually verifiable.
- Non-goals must be explicit — unstated non-goals become scope creep.
- If the plan has more than 7 steps, look for a smaller viable path first.

## Failure Classification
- **Underspecified plan**: steps are too vague to execute — break each step into a concrete action.
- **Missing verification**: the plan has no acceptance criteria — define done-when before starting.
- **Scope creep**: the plan is growing to include "nice to have" work — remove non-essential steps.

## Output Contract
- problem stated operationally
- scope and non-goals
- plan steps in order
- risks and unknowns
- verification plan
- done-when criteria
