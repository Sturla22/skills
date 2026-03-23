---
name: write-a-brief
description: Build a complete brief.md through structured discovery — problem interview, codebase exploration, requirements interview, and module sketch — then write it to the work packet. Use when starting a medium or large feature where the problem space is not yet fully understood, or when a blank template is not enough.
allowed-tools: Read, Grep, Glob, Bash
---

# Write a Brief

Guided brief-writing interview. Build the brief through discovery rather than filling in a blank template. Skip steps that are genuinely not needed, but do not skip the codebase exploration step.

## Pairs with

Run `grill-me` after this skill to stress-test the result before delegation.

## Process

### Step 1 — Problem discovery

Ask the user for a long, detailed description of:
- the problem they are trying to solve
- any intuitions they already have about solutions

Do not constrain the answer. Let them talk. Record what they say before moving on.

### Step 2 — Codebase exploration

Explore the repo to verify assertions made in step 1 and understand the current state relevant to the request:
- Find existing modules that would be affected.
- Check current test coverage and conventions.
- Look for prior art (similar patterns already in the codebase).
- Identify constraints visible in the code that the user may not have mentioned.

Do not speculate about what is there. Read files.

### Step 3 — Requirements interview

Interview the user about every significant design dependency. Walk the decision tree branch by branch (same as `grill-me`). For each question, supply a recommended answer.

Cover at minimum:
- Scope boundaries
- Non-goals (what is explicitly excluded)
- Constraints (technical, regulatory, time, resource)
- Acceptance criteria (observable, testable, done-when conditions)
- Stakeholders or callers affected
- Open risks

### Step 4 — Module sketch

Identify the main modules or subsystems that will change. For each, note:
- What it currently does (from codebase exploration, not from memory)
- What will change
- What the interface to the rest of the system looks like
- Whether there is an opportunity for a deeper module (small interface, large implementation hiding complexity)

### Step 5 — Synthesize and write

Write the brief using the template below. Write it to `docs/work/<work-id>/brief.md`. Create the work packet directory if it does not exist.

## Brief template

```markdown
# Brief: <Title>

**Work ID:** <work-id>
**Date:** <date>
**Owner:** product-owner
**Classification:** <product development | non-productized tool>

## Problem / Desired Outcome

<The problem from the requester's perspective>

## Scope

<What is included>

## Non-Goals

<What is explicitly excluded>

## Constraints

<Technical, regulatory, time, or resource constraints>

## Acceptance Criteria

<Observable, testable conditions for done>

## Delivery Class

<product development | non-productized tool>

## Affected Modules

<Modules or subsystems that will change, with current-state notes>

## Open Questions / Assumptions

<Unresolved items that need a decision before or during implementation>

## Code Drivers

<user scenario | risk | epistemic uncertainty | design intent | external obligation>
```

## Guardrails

- Do not write the brief before completing steps 1–4.
- Do not fill in acceptance criteria without making them observable and testable.
- Do not guess at current codebase state — read the files.
- Do not list modules that are not genuinely affected.
- Keep open questions visible rather than papering over uncertainty.

## Done-when

- The brief exists at `docs/work/<work-id>/brief.md`.
- All template sections are filled in or explicitly marked N/A with a reason.
- Acceptance criteria are observable and testable.
- Open questions name an owner or decision trigger.

## Output

- `docs/work/<work-id>/brief.md` (written)
- Path to the written file
- Any open questions that should be resolved before planning begins
