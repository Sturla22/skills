# AGENTS.md

This repository uses a **roles over skills** model.

## Role boundaries

Core flow roles:

- **product-owner** owns the human-facing control thread, shared understanding, success criteria, and delegation
- **planner** owns task framing, sequencing, constraints, acceptance criteria, and safe parallelism planning
- **developer** makes the smallest effective code change
- **verifier** decides whether the change is actually demonstrated
- **reviewer** looks for hidden risk, overengineering, and missing evidence
- **firmware-architect** protects interfaces, HAL boundaries, migration shape, and long-term structure

Optional specialists:

- **technical-writer** owns reader-facing clarity, doc shape, accessibility, release notes, migration/deprecation communication, and changelog quality when docs become their own lane
- **release-manager** owns release readiness, version bump synthesis, release shape, and final release communication when release coordination becomes its own lane
- **integration-engineer** owns reproducible integration, bench, HIL, environment evidence, and flake triage when real-environment work becomes its own lane
- **workflow-architect** owns evidence-based improvement of prompts, templates, skills, and roles when the operating model itself needs work

Keep one active human-facing owner. `product-owner` stays responsible for alignment with the requester. Multiple specialists may work in parallel only when `planner` has made ownership boundaries, dependencies, and integration checkpoints explicit. Specialists are internal workers by default: they return results to `product-owner`, not straight to the requester, unless the workflow explicitly says otherwise.

## Shared-understanding contract

Before delegating a non-trivial task, `product-owner` and the requester should align on:

1. Problem / desired outcome
2. Scope
3. Non-goals
4. Constraints
5. Acceptance criteria
6. Delivery class: product development or non-productized tool
7. Assumptions / open questions

Use `templates/product-brief-template.md`.

## Durable work packet

For non-trivial work, keep one durable work packet under `docs/work/<work-id>/`.

- `brief.md` is the canonical shared-understanding record. `product-owner` owns it.
- `plan.md` is the canonical execution plan. `planner` owns it.
- `status.md` is the current owner / next-action snapshot. `product-owner` owns the overall truth; the current owner updates it when the state changes.
- `evidence/` holds durable proof and investigation artifacts such as verification records, loop logs, hypotheses, and optimization scorecards.
- `handoffs/` holds role-to-role handoffs as delta records that point back to the canonical packet files.

One fact should have one durable home. Handoffs and chat should reference canonical packet files instead of restating the full context.
Store bounded process-improvement experiments separately under `docs/workflow-experiments/` so workflow changes can be tested without polluting product work packets.

## Parallel isolation

- For planned parallel write lanes, prefer isolated worktrees or equivalent isolation over one shared dirty tree when the tool supports it.
- Name each lane's owner, write surface, merge point, and worktree or isolation plan in the plan.
- Keep the active lane and worktree or isolation state visible in `status.md` when parallel work is active.

## Testing strategy

- Product development follows TDD by default.
- Prefer BDD to define acceptance criteria and observable behavior before or alongside implementation.
- Prefer the test pyramid: most coverage at unit / host-simulation level, fewer integration tests, and fewer still end-to-end or HIL checks.
- Prefer simulation-first execution for firmware behavior when the claim does not require real hardware.
- Non-productized tools do not require TDD by default, but they still require explicit verification.
- If TDD is skipped, the plan must say why and what verification replaces it.

## Bounded autonomous execution

- Use `bounded-autonomy-loop` only when the current slice is narrow, reversible enough to stop cleanly, and already has explicit done-when criteria.
- Define the stable objective, allowed write surface, checks to run every pass, and a fixed iteration or time budget before the loop starts.
- Store the loop record under `docs/work/<work-id>/evidence/bounded-autonomy-loop.md`.
- Stop on `complete`, `blocked`, or `budget exhausted`; send ambiguity or missing human decisions back to `product-owner` or `planner` instead of looping harder.
- Treat this as an optional execution mode, not as a replacement for planning, TDD, or verification.
- Do not use it for ambiguous design, unknown-cause debugging, or flaky hardware work where the environment signal is weak.

## Embedded firmware defaults

- Prefer **simulation, host tests, and characterization** before hardware-only debugging when practical.
- Keep **hardware access behind narrow interfaces**.
- Treat integration as continuous work, not a terminal phase. Bring interfaces, configurations, and integration evidence into normal iteration flow.
- Make **timing, units, ownership, and failure behavior explicit**.
- Treat **resource use** as part of correctness: stack, RAM, flash, CPU, latency, watchdog behavior, and logging overhead.
- When optimizing performance, endurance, churn, or footprint, prefer an explicit cost model: count indirect expensive operations behind seams, measure direct RAM/flash costs explicitly, assign weights where useful, and reduce the measured score without weakening required behavior.
- Treat **reboot, timeout, partial-write, corrupt-input, missing-device, and stale-data** scenarios as first-class cases.
- Do not assume a behavior is safe merely because it "usually works on the bench."

## Standard handoff contract

Store every handoff as an in-repo Markdown file under `docs/work/<work-id>/handoffs/`.
Use a non-intrusive file name such as `001-product-owner-to-planner.md`.
Use `templates/handoff-template.md`.

Every handoff should include:

1. Destination role
2. Handoff rationale
3. Pointers to canonical context: `brief.md`, `plan.md`, `status.md`, and relevant evidence
4. What changed since the previous owner or last checkpoint
5. New or changed assumptions, risks, blockers, or decisions
6. Requested next action
7. Done-when criteria for the recipient slice

## Git commit rules

- Prefer one logical change per commit. Split structural cleanup from behavioral changes.
- Commit when one logical change is complete enough to review and the relevant local checks for that slice have passed.
- Prefer committing at stable checkpoints: after a passing tidy step, after a passing refactor leaf, after the smallest verified behavior change, or after a documented docs-only update.
- Switch hats between commits. Do not mix tidy, refactor, feature, bug-fix, and broad docs churn in the same commit unless the user explicitly wants that tradeoff.
- Use careful staging to keep commits atomic. Patch or interactive staging is preferred when a file contains more than one logical change.
- Before changing direction, changing owner, or starting a new lane of work, either commit the current stable slice or discard it. Do not let half-finished state become the new baseline.
- Prefer a Conventional Commit style subject: `<type>[optional scope]: <description>`.
- Keep the subject short, imperative, and without a trailing period. Use a 50-character soft limit as a repo convention.
- Add a blank line and a body when context matters. Explain the problem, why this approach is better, and notable tradeoffs or alternatives.
- Use trailers only when relevant or required by project policy, for example `BREAKING CHANGE:`, `Co-authored-by:`, or `Signed-off-by:`.
- Keep exploratory or broken intermediate states as local scratch only. Do not share them as if they were durable history.
- Use amend or interactive rebase for local cleanup before sharing. After a commit is shared, prefer follow-up commits or explicitly coordinated history rewriting.

## Versioning and changelog

- For published releases of this repo, use Semantic Versioning.
- Treat the documented repo contract as the public API: canonical file paths under `.agents/`, generated layout expectations, role names, skill names, template names, and documented workflow conventions.
- Bump `MAJOR` for backward-incompatible changes to that contract, such as renaming a core role, moving a canonical path, or changing a required workflow in a way existing users must adapt to.
- Bump `MINOR` for backward-compatible additions, such as new roles, skills, templates, prompts, or optional workflow guidance.
- Bump `PATCH` for backward-compatible fixes, clarifications, typo fixes, and behavior-preserving corrections to existing guidance.
- Once a version is released, treat that release as immutable and publish a new version for later changes instead of rewriting the old one.
- Keep a curated root `CHANGELOG.md` for humans, not a raw commit log.
- Generated release notes can help draft a release, but they do not replace the curated changelog.
- Maintain an `Unreleased` section and group notable entries under Keep a Changelog headings such as `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`.
- When functionality is deprecated, document the deprecation in the changelog before the removal release when practical.
- On release, move `Unreleased` entries into a dated version section using ISO `YYYY-MM-DD`.

## Default role flow

1. `product-owner` establishes shared understanding with the requester.
2. `planner` reduces ambiguous or risky work to a checkable plan and identifies safe parallel lanes when they exist.
3. `developer` makes the smallest effective change.
4. `verifier` checks whether the claim is actually demonstrated.
5. `reviewer` attacks hidden risk, complexity, and weak evidence.
6. `firmware-architect` joins when interfaces, HAL boundaries, migration shape, timing, or long-term structure matter.
7. `technical-writer` joins when release notes, migration guides, deprecation notes, setup docs, doc-structure cleanup, or other reader-facing docs deserve a dedicated owner.
8. `release-manager` joins when version bump, changelog finalization, release shape, release readiness, or go/no-go communication deserves a dedicated owner.
9. `integration-engineer` joins when integration setup, HIL, flashing, bench repro, environment stability, or flaky lab signal is the bottleneck.
10. `workflow-architect` joins when repeated workflow friction, missing guidance, or possible new skills or roles need a dedicated owner.

## Default skill sequences

### Product feature work
1. `codebase-exploration`
2. `planning`
3. `requirements-and-traceability`
4. `bdd`
5. `trade-study-and-decision-analysis` when multiple credible options exist
6. `interface-contract-design`
7. `simulation-harness-first`
8. `tdd`
9. `validation-planning` when stakeholder fit needs separate evidence
10. `verification`
11. `resource-budget-review`
12. `docs-adr-updates`

### Product bug work
1. `codebase-exploration`
2. `hypothesis-driven-debugging`
3. `requirements-and-traceability` when expected behavior or ownership is unclear
4. `bdd`
5. `simulation-harness-first`
6. `tdd`
7. `verification`
8. `fault-injection-and-recovery`

### Product performance / endurance optimization
1. `codebase-exploration`
2. `planning`
3. `bdd`
4. `operation-cost-optimization`
5. `simulation-harness-first`
6. `tdd`
7. `verification`
8. `resource-budget-review`

### Non-productized tool work
1. `codebase-exploration`
2. `planning`
3. `bdd` when behavior examples improve clarity or verification
4. `tdd` if the tool is expected to become shared, long-lived, or high-risk
5. `verification`

### Release preparation
1. `codebase-exploration`
2. `release-readiness`
3. `docs-adr-updates`
4. `verification`

### Bench / HIL / integration lane
1. `codebase-exploration`
2. `lab-and-hil-reproducibility`
3. `observability-and-diagnostics`
4. `verification`
5. `fault-injection-and-recovery` when failure-path coverage matters

### System definition / concept trade
1. `requirements-and-traceability`
2. `planning`
3. `trade-study-and-decision-analysis`
4. `interface-contract-design`
5. `validation-planning`
6. `docs-adr-updates`

### Workflow evolution
1. `codebase-exploration`
2. `workflow-evolution`
3. `docs-adr-updates`
4. `verification`

### Design cleanup
1. `codebase-exploration`
2. `simplify-without-behavior-change`
3. `refactoring`
4. `verification`

### Platform migration
1. `codebase-exploration`
2. `planning`
3. `firmware-migration`
4. `hardware-abstraction`
5. `verification`
6. `safety-risk-scan`
7. `resource-budget-review`

## Behavioral defaults

- Do not delegate vague work.
- Do not run parallel work without explicit ownership boundaries.
- Do not let internal specialists silently turn into user-facing decision makers.
- Do not widen scope silently.
- Do not claim success without evidence.
- Do not run an open-ended autonomous loop without explicit budget and stop states.
- Do not run parallel write lanes in one shared dirty tree when isolated worktrees would make ownership and integration clearer.
- Do not skip TDD on product development work without making that decision explicit and visible.
- Do not treat behavior scenarios, the test pyramid, or simulation-first as optional on product development work without an explicit reason.
- Do not confuse verification with validation.
- Do not replace a concrete requirement with abstraction unless it clearly reduces complexity.
- Prefer **remove before add**, **inline before abstract**, **merge before split**, and **specialize before generalize**.
- For bug work, persist hypotheses and discriminating checks under the work packet instead of only in chat.
- For workflow changes, prefer one small mutable surface, an explicit evaluation window, and a keep / revise / revert decision.
- State what was not tested on real hardware.
- When uncertain, tighten the shared understanding, reduce the next step, and add instrumentation.
