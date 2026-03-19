# Reusable Prompts

Use these as starting points, not scripts. Fill in the bracketed context and keep the request concrete.

## Product-owner prompts

### Shared-understanding kickoff

```text
Use product-owner as the human-facing control thread for this task.

Request:
[raw request]

Please return:
- a shared-understanding brief using templates/product-brief-template.md
- a work packet rooted at `docs/work/<work-id>/`
- stakeholders, system context, and top needs that must stay visible
- any design criteria or key parameters that should stay visible next to the requirements
- the next best owner or owner set
- the public contract / SemVer / changelog impact if relevant
- the delegation handoff if the brief is strong enough

Do not delegate until scope, non-goals, constraints, acceptance criteria, and delivery class are explicit.
```

### Ambiguous request triage

```text
Use product-owner to turn this ambiguous request into something a specialist can safely execute.

Need:
- the real problem to solve
- what is in scope versus out of scope
- assumptions that need confirmation
- the smallest sensible next owner or parallel owner set
```

## General task framing

```text
Act using this repo's roles-over-skills model.
Start with product-owner if shared understanding is not already explicit.

Goal:
[what needs to be true]

Scope:
[files, modules, or behaviors in scope]

Constraints:
[timing, hardware, compatibility, safety, resource, or process constraints]

Assumptions:
[known facts and open assumptions]

Done when:
[acceptance criteria]
```

## Planner prompts

### Feature kickoff

```text
Use planner on the agreed product brief before any edits.

Goal:
[feature goal]

Please provide:
- whether this is product development or a non-productized tool
- the TDD expectation
- the relevant stakeholders, system context, and external interfaces
- the key stakeholder needs, explicit requirements, derived requirements, and constraints
- the public contract surfaces affected, if any
- the likely SemVer impact and whether `CHANGELOG.md` should change
- the key business rules, concrete examples, and open questions in BDD terms
- the key behavior scenarios in BDD terms
- the preferred test-pyramid placement for those scenarios
- the minimal configuration for the next iteration and its exit criteria
- whether a trade study is needed
- whether a separate validation plan is needed and what it should prove
- affected modules and boundaries
- likely risks and unknowns
- a smallest-safe implementation path
- any safe parallel lanes with ownership boundaries, blockers, and worktree or isolation plans
- a verification plan
- an updated `docs/work/<work-id>/plan.md`
- a handoff using templates/handoff-template.md stored under `docs/work/<work-id>/handoffs/`
```

### Multi-step change plan

```text
Use planner to break this work into small, reversible steps and parallelize safe independent work where it helps.

Change:
[describe the change]

Constraints:
[resource, interface, timing, hardware, or rollout constraints]

Bias toward:
- discovery through concrete examples before polished scenarios
- BDD-style behavior scenarios
- TDD for product development work
- the test pyramid
- remove before add
- simulation or host verification before hardware-only checks
- explicit ownership boundaries for parallel lanes
- explicit worktree or isolation plans for parallel write lanes
- explicit evidence needed at each step
```

## Developer prompts

### Smallest defensible fix

```text
Use developer to make the smallest effective change for this bug using the agreed brief as the contract.

Bug:
[symptom and expected behavior]

Scope:
[files or subsystem]

Constraints:
[must not change public behavior except for the fix]

After the change:
- summarize the patch
- state SemVer or changelog impact when relevant
- note risks
- hand off to verifier

Prefer BDD-style test names or scenarios.
If this is product development work, use TDD.
If this is a non-productized tool, state whether TDD was intentionally skipped.
```

### Behavior-preserving cleanup

```text
Use developer for a behavior-preserving cleanup only.

Target:
[file or subsystem]

Optimize for:
- less code
- clearer ownership
- fewer special cases

Do not:
- widen scope
- introduce new abstractions unless they clearly reduce complexity
- change externally visible behavior
```

### Bounded autonomous implementation loop

```text
Use planner first, then use developer with bounded-autonomy-loop only if this slice is a good fit.

Slice:
[the narrow behavior, setup, or docs slice]

Need:
- explicit done-when criteria
- one stable objective
- one allowed write surface or tightly-bounded scope
- checks to run every iteration
- a max-iteration count or time budget
- stop states: `complete`, `blocked`, or `budget exhausted`

Please return:
- whether bounded autonomy is actually a good fit here
- the loop contract: objective, write surface, checks, budget, and escalation path
- a loop record using `templates/bounded-autonomy-loop-template.md`
- the final stop state and the right next owner

If this is product development work, keep TDD inside the loop.
Do not use this for ambiguous requirements, open-ended design, or unknown-cause debugging.
```

## Verifier prompts

### Verification-first handoff

```text
Use verifier to independently check this claim against the agreed brief.

Claim:
[what the implementation is supposed to have fixed or added]

Acceptance criteria:
[observable behaviors]

Please return:
- checks run
- results
- compatibility / SemVer assessment
- residual risk
- what was not verified

Prefer reporting against behavior scenarios, then test levels.
Use templates/verification-template.md for the report shape.
```

### Hardware gap disclosure

```text
Use verifier to state what is proven in simulation or host tests versus what still needs real hardware validation.

Change:
[summary]

Focus on:
- missing hardware evidence
- timing or concurrency uncertainty
- failure-mode coverage
```

## Reviewer prompts

### Adversarial patch review

```text
Use reviewer to critique this change for hidden risk and drift from the agreed brief.

Please focus on:
- correctness risks
- hidden breaking changes or bad release classification
- overengineering
- weak evidence
- missing tests
- places where scope quietly widened

Findings first. Keep summaries brief.
```

## Firmware-architect prompts

### Interface and boundary check

```text
Use firmware-architect to review this design before implementation while preserving the agreed user-facing intent.

Design change:
[summary]

Focus on:
- HAL boundaries
- interface stability
- ownership and failure behavior
- migration shape
- timing, units, and resource impact
```

### Migration path design

```text
Use firmware-architect and planner to propose an incremental migration path.

Current state:
[legacy platform or structure]

Target state:
[desired platform or structure]

Need:
- reversible steps
- characterization checkpoints
- fallback points
- risks to interface compatibility
```

## Technical-writer prompts

### Release and migration docs

```text
Use technical-writer on this work packet.

Need:
- release notes or changelog entries
- migration or deprecation guidance
- setup, usage, or operator docs that reflect the implemented truth
- help choosing the right doc form and the clearest recommended path for the reader

Please return:
- the docs to update
- the intended reader and content form for each update
- the recommended task path or information architecture change when relevant
- any `CHANGELOG.md` changes
- migration or deprecation notes if needed
- accessibility or clarity issues worth fixing while touching the docs
- open questions that must go back to product-owner or firmware-architect

Work from the canonical work packet and evidence. Keep product docs timeless unless the content is intentionally release-specific. Do not invent behavior.
```

## Release-manager prompts

### Release readiness and versioning

```text
Use release-manager on this work packet.

Need:
- the recommended version bump
- whether this should be a pre-release, canary, or full release
- release readiness based on the current evidence
- final `CHANGELOG.md` / release-note shaping
- explicit release inputs such as commit or tag, key artifacts, and provenance or digest evidence when available
- explicit blockers or missing evidence before release

Please return:
- SemVer recommendation and why
- pre-release / final-release recommendation and why
- release-note / changelog updates needed
- release inputs and gating state
- go / no-go summary
- blockers that must be cleared before release

Work from the canonical work packet, `CHANGELOG.md`, and durable evidence. Generated notes may help, but keep the release communication curated. Do not invent readiness.
```

## Integration-engineer prompts

### Bench and HIL lane

```text
Use integration-engineer on this work packet.

Need:
- a reproducible integration, bench, flashing, or HIL setup
- durable environment or hardware evidence
- explicit capture of setup identity, steps, logs, artifacts, and blockers
- a clear split between product failures and environment failures

Please return:
- setup used, including device or board identity, fixtures, probes, key tool versions, and firmware revision
- checks run and artifacts gathered
- failure classification: product, environment, or unknown
- instability, blockers, or quarantine candidates found
- what verifier can now trust and what still remains unresolved

Work from the canonical work packet. Do not declare the overall change verified.
```

## Workflow-architect prompts

### Workflow evolution review

```text
Use workflow-architect to improve this repo's operating model from actual evidence.

Need:
- the recurring friction or confusion to address
- evidence from relevant work packets, handoffs, prompts, role usage, or Claude-native runtime behavior
- the smallest useful intervention: prompt, template, Claude-native runtime file, skill, role, or no change

Please return:
- the recurring pattern and evidence
- the chosen intervention type and why
- the minimal repo changes to make
- a workflow experiment record using `templates/workflow-experiment-template.md` when the change should be tested before being treated as settled
- SemVer / changelog impact
- the evaluation window and signals we should watch
- a keep / revise / revert recommendation or closure rule

Prefer prompt or template fixes before new skills, and new skills before new roles.
Prefer one small mutable surface per experiment.
Work from durable repo artifacts, not memory alone.
```

## Claude Code runtime prompts

### Claude worktree lane plan

```text
Use planner on this work packet and decide whether the parallel split is safe enough to deserve isolated worktrees.

Need:
- lane names
- per-lane owner
- per-lane write surface
- worktree or isolation plan for each write lane
- merge points and integration checkpoints

Please return:
- whether parallelism is worth it here
- the serialized work that must stay shared
- the worktree slug or other isolation plan for each approved lane
- updates for `docs/work/<work-id>/plan.md` and `status.md`
```

### Headless verification synthesis

```text
Use verifier to produce a concise verification summary that is suitable for headless `claude -p` use in CI or scripting.

Need:
- the main claim
- checks run
- pass/fail status
- what remains unverified
- residual risk

Keep the output compact and deterministic enough for automation.
```

## Performance optimization prompts

### Weighted operation optimization

```text
Use operation-cost-optimization on this path.

Goal:
[what behavior must still hold and what cost should go down]

Count and weight:
- [flash erases]
- [flash writes]
- [flash reads]
- [section bytes: .text / .rodata / .data / .bss]
- [stack watermark or heap usage]
- [allocations, constructions, copies, or moves]
- [other expensive operations]

Representative scenarios:
[the cases that should be measured]

Please return:
- the proposed cost model and weight rationale
- why the chosen scenarios are representative
- an optimization scorecard using `templates/optimization-scorecard-template.md`
- the counting seam or indirection point
- the direct measurement source for RAM/flash/stack when applicable
- the benchmark, PMU, compiler-report, or size-analysis tools to use
- baseline measurements to gather
- the highest-cost contributors
- the smallest behavior-preserving changes likely to reduce the score
- the verification plan for before/after behavior and score
```

## Requirements and traceability prompts

### Trace the work packet

```text
Use requirements-and-traceability on this work packet.

Need:
- the main stakeholder needs and system outcomes
- explicit requirements, derived requirements, and constraints
- trace links to behavior scenarios, design points, verification, and validation

Please return:
- an updated requirements trace using `templates/requirements-traceability-template.md`
- ambiguities or orphaned requirements
- the most important missing trace links
```

## Trade-study prompts

### Compare viable options

```text
Use trade-study-and-decision-analysis on this decision.

Decision:
[what choice needs to be made]

Need:
- real options at the same abstraction level
- explicit criteria
- assumptions and reversibility
- one recommendation with consequences

Please return:
- a trade study using `templates/trade-study-template.md`
- the recommendation
- the assumption most likely to change the decision
```

## Validation-planning prompts

### Stakeholder-fit plan

```text
Use validation-planning on this work packet.

Need:
- the stakeholder outcome this work is meant to improve
- measures of effectiveness or performance
- validation scenarios
- the evidence source and what will still remain unvalidated

Please return:
- a validation record using `templates/validation-template.md`
- the validation question
- the planned evidence source
- deferred validation gaps if any
```

## Bug work prompts

### Hypothesis-driven debug request

```text
Use hypothesis-driven-debugging on this issue.

Symptom:
[what fails]

Known evidence:
[logs, tests, hardware observations]

Please provide:
- ranked hypotheses
- the next discriminating checks
- one file per hypothesis under `docs/work/<work-id>/evidence/hypotheses/`
- the smallest instrumentation needed
- whether host simulation can reduce uncertainty first

Use `templates/hypothesis-template.md` for each hypothesis record and update each file with what was tested, how it was tested, and the result.
```

### Failure-path coverage

```text
Investigate this bug with a safety-aware lens.

Also check:
- timeout behavior
- partial-write or corrupt-input handling
- missing-device behavior
- stale-data or reboot edge cases
```

## Documentation prompts

### Update docs after change

```text
Use docs-adr-updates after this implementation.

Change summary:
[summary]

Please update:
- any stale workflow docs
- `CHANGELOG.md` if the change is notable to downstream users
- setup or usage guidance
- ADR notes if the design truth changed
- the audience and doc form for each updated doc
- the recommended path if task guidance is involved
- accessibility or scannability issues that should be fixed while touching the docs

Keep docs aligned with what is actually implemented. Keep durable docs timeless unless the content is intentionally release-specific.
```

### Prepare release notes

```text
Prepare the next release notes for this repo.

Need:
- the recommended SemVer bump and why
- the notable `Unreleased` entries to add or refine in CHANGELOG.md
- any breaking changes or deprecations that need to be called out explicitly
- any docs or templates that should change before release

Treat the documented repo contract as the public API.
Use a curated changelog, not a commit log dump.
```

## Release-readiness prompts

### Release gate and shape

```text
Use release-readiness on this work packet.

Need:
- the honest SemVer classification
- whether this should be a pre-release, canary, or full release
- the exact release candidate inputs
- gate status, blockers, and missing evidence
- curated release communication

Please return:
- candidate commit or tag and key artifact identity
- version or pre-release recommendation and why
- gate status
- changelog or release-note updates needed
- go / no-go recommendation
```

## Lab and HIL reproducibility prompts

### Reproducible bench lane

```text
Use lab-and-hil-reproducibility on this work packet.

Need:
- the exact setup identity
- repeatable setup and flashing steps
- durable logs or artifacts
- a clear split between product failures and environment failures
- quarantine guidance if the lane is flaky

Please return:
- board or device identity, fixtures, probes, firmware revision, and key tool versions
- repeatable run steps
- checks run and artifacts gathered
- failure classification
- blockers, instability, or quarantine candidates
- the next improvement that would reduce bench cost
```

## Git commit prompts

### Draft a commit message

```text
Draft a commit message for these staged changes.

Need:
- one logical commit only
- a short imperative subject
- Conventional Commit style if it fits
- a body only if the why, tradeoffs, or alternatives are not obvious

If the staged diff looks like more than one logical change, say so instead of forcing a message.
```

### Suggest commit boundaries

```text
Look at this work-in-progress and suggest commit boundaries.

Need:
- the best next point to commit
- whether the current state is stable enough to commit yet
- which changes should be split into separate commits
- what verification should happen before each commit

Prefer boundaries that keep each commit atomic, reviewable, and easy to bisect.
```

## Handoff prompts

### Structured handoff

```text
Before switching roles, write a handoff using templates/handoff-template.md.
Store it under `docs/work/<work-id>/handoffs/`.

Include:
- pointers to the canonical brief, plan, and status files
- what changed since the last checkpoint
- impact analysis for downstream requirements, interfaces, tests, validation, or docs
- evidence gathered so far
- changed assumptions or risks
- open risks
- requested next action
- done-when criteria
```
