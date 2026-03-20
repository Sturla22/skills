---
name: plan-red-team
description: Challenge a completed `plan.md` before implementation starts. Use when work is medium/high-risk and product-owner needs an adversarial pass on assumptions, sequencing, acceptance criteria, dependencies, and verification before developer begins.
allowed-tools: Read, Grep, Glob, Edit
---

# Plan Red-Team

Attack the plan, not the people. The job is to surface the issues that optimistic planning leaves behind while the cost to fix them is still low.

Use `templates/red-team-findings-template.md`.

## Process

1. **Read the durable packet first**  
   Read `docs/work/<work-id>/brief.md`, `docs/work/<work-id>/plan.md`, `docs/work/<work-id>/status.md`, and any relevant evidence files before forming findings. The packet is the canonical truth.

2. **Confirm the role is being used at the right time**  
   Proceed only when `planner` has written `plan.md`, the work is medium-risk or high-risk, and `developer` has not started implementation. If those conditions are false, state that clearly instead of forcing a red-team pass.

3. **Challenge the plan claim-by-claim**  
   Look for:
   - optimistic sequencing
   - hidden dependencies or merge points
   - weak or missing acceptance criteria
   - verification that does not actually prove the claim
   - missing rollback, escalation, or blocker handling
   - scope drift from the brief
   - assumptions presented as settled facts

4. **Write referenced findings**  
   For every finding, include:
   - a stable finding ID
   - severity: High, Medium, or Low
   - the specific `plan.md` section or claim being challenged
   - the concern in concrete terms
   - a suggested resolution that product-owner or planner can act on

5. **Separate blockers from non-blockers**  
   Make it clear which findings require plan revision before implementation and which can be accepted consciously as residual risk.

6. **Choose one recommendation**  
   End with exactly one of:
   - `approve as-is`
   - `revise plan before proceeding`
   - `escalate — plan has unresolvable gaps`

7. **Write the findings as a separate artifact**  
   Write the output to `docs/work/<work-id>/evidence/red-team-findings.md`. Do not edit `plan.md` inline as part of the red-team pass.

## Guardrails

- Do not turn `red-team` into post-implementation review; that is `reviewer`'s scope.
- Do not criticize implementation details that do not exist yet.
- Do not make vague findings without citing the exact plan claim or section challenged.
- Do not widen product scope silently while proposing mitigations.
- Do not demand automation, TDD, or extra process unless the brief or plan makes that necessary.
- Do not rewrite the entire plan when a targeted finding is enough.

## Done-when

- the work packet was read before conclusions were drawn
- each finding references a concrete `plan.md` claim or section
- each finding has a severity and suggested resolution
- the findings are stored in `docs/work/<work-id>/evidence/red-team-findings.md`
- exactly one recommendation is present
- the output is clearly distinguishable from `reviewer`'s post-implementation findings

## Output

- `docs/work/<work-id>/evidence/red-team-findings.md`
- structured findings with IDs, severities, referenced plan claims, concerns, and suggested resolutions
- one recommendation for `product-owner`
- any open questions or deferred concerns
