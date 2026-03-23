---
name: story-loop
description: Run a list of user stories autonomously, implementing each with the smallest effective change and verifying with automated checks before moving on. Use when a planner-defined story list has explicit acceptance criteria and automated checks (tests, lint, build) that can verify each story.
allowed-tools: Read, Grep, Glob, Edit, MultiEdit, Bash
---

# Story Loop

Concrete instantiation of bounded-autonomy-loop for story-driven work (the Ralph Loop pattern: relentlessly failing but persistent until all stories are done or blocked).

## Prerequisites

Before this skill is invoked, the planner must define:
- the story list file path
- the check commands (tests, lint, build) to run after each story
- the max iteration budget (total passes across all stories)

Stories must have explicit acceptance criteria. Do not invoke this skill on a vague story list.

## Process

1. **Read the story list.** Locate all stories with `status: open`. If none are open, report complete.

2. **Pick the first open story.** Work stories in the order they appear in the list. Do not skip ahead.

3. **Implement the story using the smallest effective change.** Follow TDD inside the loop for product development work: write a failing test, make the smallest change to pass it, then clean up while green.

4. **Run the check commands.** Use exactly the commands defined by the planner. Do not substitute or skip.

5. **If checks pass:**
   - Mark the story `status: done` in the story list file.
   - Commit with the story ID in the commit subject (e.g., `feat(S-03): add sensor fault flag`).
   - Move to the next open story. Reset the per-story failure counter.

6. **If checks fail:**
   - Read the error output. Identify the root cause.
   - Fix the code. Re-run the checks.
   - Repeat up to 3 attempts on the same story.
   - If checks fail a 4th time on the same story: stop. Add `status: blocked` to the story with the full error message and the last hypothesis. Return to product-owner.

7. **Repeat** until all stories are `done` or `blocked`, or the iteration budget is exhausted.

8. **If budget is exhausted before all stories are resolved:**
   - Mark remaining open stories as `status: budget-exhausted`.
   - Report the final state to product-owner with counts: done, blocked, budget-exhausted.

## Safety contract

- Do not widen the write surface beyond what the planner defined.
- Do not change story acceptance criteria during the loop — that is replanning.
- If a story's behavior conflicts with an existing passing test, stop and escalate rather than deleting the test.
- Keep the story list file accurate at all times — it is the durable record of loop state.

## Done-when

- All stories are marked `done` or `blocked`.
- A commit exists for each completed story.
- Blocked stories have an escalation note with the error and last hypothesis.
- The loop record at `docs/work/<work-id>/evidence/bounded-autonomy-loop.md` is updated with the final stop state.

## Output

- Updated story list (status per story)
- Commit log (one commit per completed story)
- Blocked stories with escalation notes
- Final stop state: `complete`, `blocked`, or `budget exhausted`
