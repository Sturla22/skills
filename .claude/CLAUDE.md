# Claude Code Project Instructions

See @../AGENTS.md for the role model and default workflow order.

## Project goals

This starter repo is optimized for embedded firmware teams that want:
- a product-owner front door that aligns on intent before delegation
- reusable skills instead of giant prompts
- clear separation between planning, implementation, verification, and review
- optional technical-writing support when reader-facing docs, doc-structure cleanup, or release communication deserve their own lane
- optional release-management support when version bump and release readiness deserve their own lane
- optional integration-engineering support when bench, HIL, or environment execution becomes its own lane
- optional workflow-architecture support when repeated process friction or missing reusable guidance becomes its own lane
- bounded autonomous execution for narrow, auto-checkable slices with explicit budgets and stop states
- Claude-native runtime defaults through `.claude/settings.json`, `.claude/rules/`, `.claude/hooks/`, `.claude/output-styles/`, and `.mcp.json`
- behavior-first testing guidance with BDD, TDD, the test pyramid, and simulation-first
- interfaces that survive platform migration
- host-side simulation and characterization where possible
- explicit safety and resource thinking

## Replace these placeholders for your real project

### Build commands
- Primary configure: `cmake -S . -B build`
- Primary build: `cmake --build build`
- Primary test: `ctest --test-dir build --output-on-failure`
- Lint / static analysis: `TODO`
- Host simulation tests: `TODO`
- Hardware integration tests: `TODO`

### Key directories
- Application code: `src/`
- HAL / platform: `platform/`
- Drivers: `drivers/`
- Tests: `tests/`
- Docs / ADRs: `docs/`

## Working rules

- Start non-trivial work with a shared-understanding brief in `docs/work/<work-id>/brief.md` or an equivalent durable summary.
- In Claude Code, let `.claude/settings.json` default the main thread to `product-owner` and Plan Mode unless there is a deliberate local override.
- Let `product-owner` own the human-facing thread and delegate explicitly; parallel specialists are fine when the planner has defined boundaries, dependencies, and integration checkpoints.
- Use `.claude/rules/` for modular, path-scoped Claude Code rules instead of growing one giant extra memory file.
- Classify the work as product development or a non-productized tool before implementation starts.
- Product development follows TDD by default. Non-productized tools may use lighter-weight verification when the plan says so explicitly.
- Prefer BDD-style behavior scenarios for acceptance criteria and test naming.
- Make stakeholder needs, system context, and critical requirements explicit when the work is complex enough that handoffs could drift.
- Use `requirements-and-traceability` when the main needs, constraints, or acceptance logic need durable linkage across the work.
- Use `trade-study-and-decision-analysis` when more than one credible design or rollout option exists.
- Prefer the test pyramid and simulation-first host checks before slower or hardware-only testing when the claim allows it.
- Use `bounded-autonomy-loop` only when the slice is well-scoped, the done-when is explicit, the checks can run every pass, and a fixed budget and escalation path are defined up front.
- Use `validation-planning` when implementation correctness alone will not show that the work solved the right problem.
- For performance, endurance, or footprint work, prefer an explicit cost model over intuition-only tuning: count indirect costs, measure direct RAM/flash costs, and use weighting when it helps rank tradeoffs.
- Read the relevant skill before doing a complex task.
- Prefer the smallest useful diff.
- Prefer one logical change per commit, and use patch staging when needed to keep commits atomic.
- Prefer committing at stable checkpoints: after the current slice is coherent, reviewed locally, and verified at the right level for that slice.
- Switch tidy/refactor/behavioral hats between commits, not inside one commit.
- Prefer a short imperative commit subject, ideally in Conventional Commit form, with a body when the why or tradeoffs are not obvious.
- Treat Semantic Versioning as the default release policy for this repo's documented contract.
- Use a durable work packet under `docs/work/<work-id>/` for briefs, plans, status, evidence, and handoffs instead of scattering the same context across chat.
- Use `release-readiness` when release preparation, SemVer classification, or go / no-go synthesis becomes real work instead of an afterthought.
- Use `lab-and-hil-reproducibility` when bench or HIL evidence needs setup identity, repeatable steps, and honest flake classification.
- Use `workflow-evolution` when the process itself needs evidence-based improvement and the smallest intervention must be chosen deliberately.
- When evolving the workflow, prefer one small mutable surface, an explicit evaluation window, and a keep / revise / revert decision recorded under `docs/workflow-experiments/`.
- Prefer isolated worktrees for planner-approved parallel write lanes, and keep the lane plus worktree or isolation state visible in `plan.md` and `status.md`.
- Use `.mcp.json` for project-shared MCP servers, and keep secrets in environment variables rather than in repo-tracked config.
- Use headless `claude -p` flows for planning, review, verification synthesis, and CI-friendly reporting when that helps.
- If you add a Claude output style, keep `keep-coding-instructions: true` unless the style is intentionally non-coding.
- When reader-facing docs, doc-structure cleanup, or release communication become a substantial lane, delegate that lane to `technical-writer`.
- When release readiness, version bump, and final release communication become a substantial lane, delegate that lane to `release-manager`.
- When bench, HIL, flashing, or integration-environment work becomes a substantial lane, delegate that lane to `integration-engineer`.
- When repeated workflow friction or likely changes to prompts, templates, skills, or roles become a substantial lane, delegate that lane to `workflow-architect`.
- When an external knowledge gap — datasheets, specs, standards, errata, or feasibility signals — must be closed before planning can proceed, delegate that lane to `researcher`.
- Log any bounded autonomy loop under `docs/work/<work-id>/evidence/bounded-autonomy-loop.md` and stop on `complete`, `blocked`, or `budget exhausted`.
- Before changing hardware-facing code, make the interface and test seam explicit.
- Before risky refactors, add characterization tests.
- Before claiming a bug is fixed, prove the original symptom was reproducible or at least well-characterized.
- Update docs and `CHANGELOG.md` when architecture, contracts, failure behavior, migration paths, or release-relevant behavior change.

## Firmware-specific rules

- Keep units explicit in names, comments, or types.
- Keep ISR / thread / task context assumptions explicit.
- Avoid hidden global state.
- Avoid speculative abstraction and future-proofing with no near-term caller.
- Be conservative with dynamic allocation, blocking behavior, and retry loops.
- Prefer assertions for violated internal invariants and explicit error returns for expected external failures.
- Log at boundaries that matter, not everywhere.

## Deliverable expectations

Every substantial task should leave behind:
- a shared-understanding brief
- a plan or rationale
- a current status snapshot
- a work packet under `docs/work/<work-id>/` when the task is non-trivial
- a named worktree or other isolation plan in `plan.md` and `status.md` when parallel write lanes were used
- code or doc changes
- a commit history that stays readable when the work is committed
- changelog updates when the change is notable to downstream users of the repo
- requirements trace or trade-study notes when the work needed systems-level clarification
- reader-facing docs or migration notes, shaped for the right audience and doc form, when a dedicated docs lane was part of the work
- validation notes when a stakeholder-fit question existed for the work
- release-readiness notes when a dedicated release lane was part of the work
- integration or hardware evidence when a dedicated integration lane was part of the work
- workflow-evolution notes when a dedicated process-improvement lane was part of the work
- a bounded-autonomy loop record when that execution mode was used
- evidence of verification
- the stated TDD expectation and whether it was followed
- a short statement of residual risk
