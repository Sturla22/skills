---
name: grill-me
description: Stress-test a brief or plan through relentless structured interrogation, walking every significant decision branch with a recommended answer before delegation begins. Use when product-owner wants to stress-test a brief, when planner wants to challenge a plan, or when the user explicitly says "grill me."
allowed-tools: Read, Grep, Glob, Bash
---

# Grill Me

Conduct a relentless structured interrogation of a brief or plan to reach genuine shared understanding before delegation begins. The goal is surfacing hidden assumptions and unresolved branches — not surface-level agreement.

## Process

1. **Read the document in full.** If the brief or plan is not in context, ask for it before proceeding.

2. **Map the decision tree.** Identify every significant choice, assumption, constraint, and dependency in the document. Include scope boundaries, acceptance criteria ambiguities, technical constraints, and open questions.

3. **Walk each branch in dependency order.** Resolve prerequisite decisions before dependent ones. Do not jump ahead.

4. **For each branch:**
   - Ask ONE question at a time. Do not bundle multiple questions.
   - Supply a recommended answer with your question: "I'd suggest X because Y — does that match your intent?"
   - If the codebase can answer the question (current state, existing patterns, constraints), read the relevant files FIRST instead of asking.
   - If an answer exposes a new branch, follow it before moving on.

5. **Accept only concrete answers.** If an answer is vague, follow up. Do not move to the next branch on an unresolved answer.

6. **Continue until** all significant branches are resolved or the user says stop.

7. **Produce a summary paragraph** covering: decisions confirmed, assumptions validated, risks surfaced, and any unresolved items. This summary is the handoff record — it should be durable enough to paste into `brief.md` or `plan.md`.

## Guardrails

- Do not ask multiple questions at once.
- Do not accept vague answers — follow up if the answer does not resolve the branch.
- Do not propose solutions during the interrogation — stay in discovery mode.
- Do not skip branches that seem obvious — obvious branches hide the most assumptions.
- Stay in grill-me mode until the user says stop or all branches are resolved. Do not pre-emptively move to implementation.

## Done-when

- All significant decision branches are resolved or explicitly deferred.
- A summary paragraph exists that could stand alone as a shared understanding record.
- Any unresolved items are named with a clear owner or next action.

## Output

- Resolved decisions (one per branch)
- Validated assumptions
- Risks surfaced
- Unresolved items with owner or next action
- Summary paragraph
