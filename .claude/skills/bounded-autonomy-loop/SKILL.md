---
name: bounded-autonomy-loop
description: Run a narrow implementation or setup slice as a fixed-budget self-correcting loop with explicit done-when criteria, automated checks, and durable stop conditions. Use when the task is already well-scoped, the core objective can stay stable across iterations, and the loop can stop cleanly as complete, blocked, or budget exhausted.
allowed-tools: Read, Grep, Glob, Bash
---

# Bounded Autonomy Loop

Use a Ralph-style loop only when the work is already well framed.
This is an execution mode, not a substitute for `product-owner`, `planner`, `tdd`, or `verification`.

## Good fits

- a narrow implementation slice with explicit acceptance criteria
- TDD work where the next behavior is clear and tests can run every pass
- contained cleanup or setup automation with clear pass / fail checks
- greenfield or isolated tasks where file state persists and automated feedback is cheap

## Poor fits

- ambiguous requirements or weak shared understanding
- open-ended design or architecture tradeoffs
- debugging with unknown cause and weak discriminating checks
- flaky bench or HIL work where environment failures dominate
- tasks that require repeated human judgment or multiple moving completion conditions

## Tracking convention

- Create or reuse the work packet under `docs/work/<work-id>/`.
- Use `templates/bounded-autonomy-loop-template.md`.
- Store the loop record at `docs/work/<work-id>/evidence/bounded-autonomy-loop.md`.
- Update the loop record each iteration or checkpoint with what changed, what checks ran, and why the loop continues or stops.

## Process

1. **Read the packet and confirm the slice is truly bounded** — start from `brief.md`, `plan.md`, and `status.md`.
   ```
   Read("docs/work/<work-id>/brief.md"), Read("docs/work/<work-id>/plan.md"), Read("docs/work/<work-id>/status.md"), Glob("docs/work/<work-id>/evidence/**")
   ```

2. **Lock the loop contract before starting** — make these explicit:
   - stable objective
   - done-when
   - allowed write surface
   - checks to run every iteration
   - max iterations or time budget
   - stop states: `complete`, `blocked`, `budget exhausted`
   - escalation target when blocked

3. **Keep the objective stable across iterations** — refine tactics, not the goal. If the success condition changes, stop and replan.

4. **Make one small attempt, then run checks** — each iteration should change one narrow thing, run the planned checks, and let the result drive the next attempt.
   - For product development work, keep TDD inside the loop: failing test, smallest pass, cleanup while green.
   - For non-productized tools, keep the agreed replacement verification inside the loop.

5. **Use failures as data, not as permission to thrash** — if the checks stop being discriminating, pause and improve the checks or exit `blocked`.

6. **Record the iteration durably** — capture the change attempted, checks run, outcome, artifacts, and next adjustment in the loop record.

7. **Stop immediately on a terminal state** — the valid terminal states are:
   - `complete`
   - `blocked`
   - `budget exhausted`

8. **Hand off honestly** — return the final stop state, evidence, and next recommendation to `verifier` or `product-owner`.

## Guardrails

- Do not start without explicit done-when criteria.
- Do not run without a max iteration count or time budget.
- Do not let the loop widen the write surface without handing back to `planner`.
- Do not use a vague completion promise like "done when it looks good."
- Do not let the loop hide missing human decisions or product tradeoffs.
- Do not use this as cover for endless retries on flaky hardware or unknown-cause bugs.
- Do not treat the loop as self-verification; `verifier` still owns the verdict.
- If the task no longer matches the original bounded objective, stop and replan.

## When it stalls

- **Checks fail for a new reason** — tighten the slice or hand back to `planner`.
- **Requirements drift appears** — stop and return to `product-owner`.
- **Budget is nearly gone** — spend the remaining budget on one more discriminating attempt or on a good blocked handoff, not on repetition.
- **The loop needs a different success condition** — that is replanning, not another iteration.

## Done-when

- the loop contract is explicit
- the iteration log is durable
- the final stop state is explicit
- evidence exists for what changed and what passed or failed
- the next owner and escalation reason are clear

## Output

- loop contract
- iteration log
- final stop state
- checks run and results
- blockers or exhausted-budget note
- next recommended owner
