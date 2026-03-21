---
name: planning
description: Produce a concrete, staged plan with explicit verification before implementation. Use when a request is ambiguous, multiple implementation options exist, work crosses modules or layers, or risk needs to be understood before code changes.
allowed-tools: Read, Grep, Glob, Bash
---

# Planning

Produce a low-risk, checkable plan.

## Process

1. **Read the relevant context** — understand the current state before proposing changes.
   ```
   Glob("**/{README*,CLAUDE.md,docs/**}"), Read("<relevant-source-files>")
   ```

2. **Restate the problem operationally** — what must be true when the work is done?

3. **Classify the work** — state whether this is product development or a non-productized tool. Product development plans must include TDD. Tooling plans may omit TDD only with explicit justification and replacement verification.

4. **Define end state and non-goals** — be explicit about what is out of scope.

5. **State system context and stakeholders** — identify who is affected, which external systems or interfaces matter, and what lifecycle stage or rollout context the work sits in.

6. **Identify contract and release impact** — name which documented repo contract surfaces, if any, will change. State the likely SemVer impact (`MAJOR`, `MINOR`, `PATCH`, or no release impact) and whether `CHANGELOG.md` should change.

7. **Make requirements explicit enough to plan from** — identify stakeholder needs, explicit requirements, derived requirements, constraints, and assumptions that must be kept visible across the work.

8. **Define the preferred test and validation strategy** — name the key behavior scenarios in BDD terms, place them on the test pyramid, prefer simulation-first execution when hardware is not essential, and note whether a separate validation plan is needed to show fitness for purpose.

9. **Handle unknowns with spikes** — for any step with excessive uncertainty, replace it with a time-boxed spike (1–2 days max, one focused question, output is a decision not code). Schedule spikes before the stories that depend on them.

10. **Plan a walking skeleton first** — identify the thinnest end-to-end slice that proves all architectural components connect. Build that first; grow functionality on top. This surfaces integration risks before feature investment.

11. **Define the minimal configuration and exit criteria for the next iteration** — state the smallest configuration, system level, or milestone slice that is worth building now, and the concrete exit criteria that would justify moving on.

12. **Break into ordered steps and safe parallel lanes** — each step should be independently deliverable and verifiable. Apply INVEST: each step is **I**ndependent, **N**egotiable, **V**aluable, **E**stimable, **S**mall, **T**estable. Split anything that fails "Small" or "Testable". When two steps are truly independent, name them as parallel lanes instead of serializing by default.

13. **Define ownership and dependencies for parallel work** — for each parallel lane, state the owner, boundaries, blockers, expected integration point, and what must stay serialized. If the tool supports isolated worktrees, name the intended worktree or other isolation for each write lane.

14. **Name assumptions and unknowns** — flag anything that could invalidate the plan. Biggest risks get mitigation first (risk-driven ordering).

15. **Define acceptance criteria and traceability** — state how each step will be verified before proceeding. Product development steps should identify the failing-test-first path. Non-productized tooling steps that skip TDD should say what verification replaces it. Tie each key behavior scenario to its planned test level, and note the requirement or stakeholder need each step advances. "Done when" must be concrete and measurable; no "should be fast" or "should be easy".

## What makes a plan good enough to start
- Biggest risks each have an assigned mitigation or spike.
- A walking skeleton is planned for the first deliverable.
- The minimal configuration for the next iteration and its exit criteria are explicit.
- Near-term steps pass INVEST.
- Safe parallel opportunities are named with clear ownership and merge points.
- Parallel write lanes also have an explicit worktree or other isolation plan when the tool supports it.
- Stakeholders, external interfaces, and top technical risks are explicit.
- The plan explicitly says whether TDD is required or intentionally waived because the work is non-productized tooling.
- The key behavior scenarios and their planned test levels are explicit.
- The requirement / stakeholder-need trace for the main steps is visible.
- Validation signals are explicit when user-fit matters.
- The contract surfaces touched, SemVer expectation, and changelog expectation are explicit.
- Acceptance criteria are written for at least the first two steps.
- Hardware/external dependencies are mapped with estimated unblock dates.

## Guardrails
- Do not start implementation until the plan is agreed.
- If two approaches have similar risk, prefer the more reversible one.
- Do not include steps that cannot be verified — replace with a spike or investigation step.
- Keep the plan at the level of steps, not implementation details.
- Do not omit TDD from product development plans.
- Do not skip BDD-style behavior definition on product development work.
- Do not confuse verification planning with validation planning.
- Do not treat release impact as an afterthought when the documented contract changes.
- Do not force parallelism when coordination cost exceeds the benefit.
- Do not parallelize steps that share the same write surface unless boundaries are explicit and conflict risk is acceptable.
- Do not parallelize write-heavy lanes without naming the isolation plan when isolated worktrees would materially reduce conflict.
- For embedded projects: plan HAL boundary definition in the first step to decouple firmware development from hardware availability.
- For embedded projects: name the target Pitchfork directory (`src/`, `include/`, `libs/<name>/`, `tests/`) for every new file or module in the plan before implementation starts. Flag misplaced files as structural debt in a separate tidy step.

## When planning stalls
- **Scope is unclear** — narrow to one concrete deliverable and plan that first.
- **Too many unknowns** — add a time-boxed spike before the main plan.
- **Approaches are incommensurable** — present both with explicit trade-offs and ask the user to choose.
- **Parallelism seems possible but fuzzy** — keep discovery or interface work serial until ownership boundaries are clear, then split implementation lanes.

## Done-when
- scope is explicit
- steps are ordered, and parallelizable work is explicit where appropriate
- acceptance criteria are concrete
- the TDD expectation is explicit
- the BDD / pyramid / simulation-first strategy is explicit
- stakeholders, requirements, and validation intent are explicit where relevant
- the release / compatibility impact is explicit
- risks and spikes are identified

## Output
- problem (operational statement)
- delivery class and TDD expectation
- stakeholders, system context, and lifecycle context
- contract surfaces touched and SemVer / changelog expectation
- requirements / constraints / assumptions that must stay visible
- behavior scenarios and test strategy
- validation signals or deferred validation notes
- scope and non-goals
- walking skeleton description
- minimal configuration / exit criteria
- plan steps (with acceptance criteria)
- parallel lanes, boundaries, and blockers
- worktree or isolation plan for active parallel write lanes
- risks and unknowns
- spikes (if any)
