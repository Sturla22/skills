# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `tools/cli.py new-postmortem <work-id>` creates numbered postmortem records under `docs/work/<work-id>/evidence/`, and `tools/cli.py check-debt` reports tracked debt items from `docs/tech-debt.md` by status.
- A lightweight stdlib-only pre-commit secret detector now lives at `tools/dev/detect_secrets.py`. The local `detect-secrets` hook scans staged text files for long base64/hex blobs, common API/password patterns, AWS keys, and private-key headers while skipping markdown, lockfiles, binary files, and explicit allowlist comments.
- Workflow guidance now explicitly prefers supported CLI commands over direct file edits when the CLI already models the operation, especially for work packets and related artifacts. `AGENTS.md`, `docs/operating-model.md`, `.github/copilot-instructions.md`, and `README.md` now point users toward `tools/cli.py new-work`, `new-handoff`, `new-scenarios`, `check-work`, and `list-work` before manual file creation.
- Copilot-specific repo guidance now explicitly biases the agent toward narrow, staged patches instead of large all-at-once edits. `.github/copilot-instructions.md` now tells Copilot to keep the active write surface small, and to shrink scope after a failed patch attempt instead of escalating into a broader retry. `docs/workflow-experiments/EXP-007-bias-copilot-toward-small-patches.md` records the evaluation window.
- The operating model now states explicitly that a bare requester instruction to `commit` means create one or more logical commits, not one umbrella commit, unless the requester explicitly asks for a single combined commit. `AGENTS.md` and `docs/operating-model.md` now encode that clarification, and `docs/workflow-experiments/EXP-006-interpret-commit-as-logical-commits.md` records the evaluation window.
- Copilot custom-agent generation now supports per-role model selection from canonical role specs: `copilot_model` values in `.agents/agents/*.toml` are emitted as `model:` in `.github/agents/*.agent.md`. The current repo policy is explicit: non-review high-reasoning roles use `gpt-5.4`, other non-review roles use `gpt-5.4-mini`, high-reasoning review roles use `claude-opus-4.6`, and other review roles use `claude-sonnet-4.6`. Default non-agent Copilot chat still cannot be forced repo-wide.
- The operating model now states explicitly that tool-local scratch artifacts such as `~/.copilot/session-state/` are not canonical substitutes for `docs/work/<work-id>/brief.md`, `plan.md`, `status.md`, `evidence/`, or `handoffs/`. Canonical `product-owner` and `planner` roles, `AGENTS.md`, `docs/operating-model.md`, Copilot repo instructions, the Copilot VS Code playbook, and Copilot first-run prompts now all reinforce that rule.
- Copilot support now treats the existing path-specific instruction files under `.github/instructions/` as a first-class part of the repo-tracked support surface. `tools/cli.py doctor --tool copilot`, `docs/copilot-vscode-playbook.md`, `docs/compatibility.md`, `README.md`, and `.github/copilot-instructions.md` now surface and verify that layer more explicitly.
- `make check-static-analysis`, `tools/ci/check-static-analysis.py`, and `extras/cmake-nrf52840-template/.clang-tidy` establish the repo's first concrete C++ static-analysis baseline for the starter. The recommendation for this repo is now: use preset-specific compile databases in-editor, use `make check-static-analysis` for local gating, and keep CI on the same repo-owned command instead of introducing a separate analyzer service or thicker workflow YAML.
- Repo guidance now states a script-language preference: when repo-owned automation grows beyond a short shell wrapper, prefer Python over Bash. Small wrappers around package installs or linear command sequences may stay in shell.
- `.pre-commit-config.yaml`, `make install-pre-commit`, `make run-pre-commit`, and `make check-pre-commit-config` now wire the `pre-commit` framework into the repo. The local `static-analysis` hook runs `make check-static-analysis`, while CI still runs the analyzer directly and only validates the hook config.
- `extras/cmake-nrf52840-template/.clang-format`, `make format-cpp`, `make check-clang-format`, `tools/dev/run_clang_format.py`, and `tools/ci/check-clang-format.py` add a concrete C/C++ formatting baseline for the starter. The `pre-commit` hook now auto-formats changed starter C/C++ files, and CI enforces formatting through a non-mutating check.
- `extras/cmake-nrf52840-template/`: a concrete embedded CMake starter with checked-in host and Arm cross-build presets, a `gcc-arm-none-eabi` toolchain-file example, configure-time architecture enforcement, a semihosted nRF52840 hello-world firmware target, and host-side verification including a negative test that proves invalid layer dependencies are rejected. `README.md` and `docs/firmware-playbook.md` now point to this starter as the repo's concrete embedded CMake baseline.
- `.github/workflows/check-agent-sync.yml` now also configures, builds, and tests the `extras/cmake-nrf52840-template/` host preset and cross-builds the nRF52840 firmware preset after installing the GNU Arm Embedded toolchain packages on the runner.
- CI automation now prefers thin GitHub Actions YAML that delegates substantive setup and verification logic to repo-tracked scripts or Make targets under `tools/`. `check-agent-sync.yml` now uses `make ci-bootstrap-ubuntu` and `make ci-checks`, backed by `tools/ci/bootstrap-ubuntu.sh` and `tools/ci/check-cmake-starter.sh`.
- `tools/cli.py check-layout` now also flags any non-dot top-level directory that is not in the PFL-recognised set (`src`, `include`, `libs`, `tests`, `extras`, `data`, `tools`, `docs`, `external`, `build`). Dot directories (`.agents/`, `.claude/`, `.github/`, etc.) are intentionally excluded — PFL does not restrict hidden directories. `tests/fixtures/pitchfork-layout/violations/` gains a `mymodule/` directory to exercise the new check; four-violation output is now: root-source, test-outside-tests, libs-no-src, unknown-dir.
- `make check-layout` and a corresponding GitHub Actions step run `check-layout` on every push and pull request, keeping Pitchfork compliance in CI from day one.
- `tools/cli.py check-layout` enforces the Pitchfork C++ layout with three checks: source/header files at repo root, test files outside `tests/`, and `libs/<name>/` subdirectories missing `src/`. Exit 0 = clean; exit 1 = violations with grouped output. Fixtures at `tests/fixtures/pitchfork-layout/{valid,violations}/` cover all paths.
- Pitchfork C++ project layout directive: `CLAUDE.md` key directories updated to the Pitchfork shape (`src/`, `include/`, `libs/`, `tests/`, `external/`, `tools/`, `data/`, `extras/`, `build/`); working rule added requiring Pitchfork compliance; `AGENTS.md` behavioral default added; `planning` skill guardrail added requiring planner to name target Pitchfork directory for every new file; path-scoped `.agents/rules/pitchfork-layout.md` provides the full spec (directory map, header placement choice, embedded conventions, planner/developer rules) active whenever source paths are in context; `docs/firmware-playbook.md` gains a **Project Layout** reference section.
- Project-level risk catalog: `RK-NNN` IDs in `docs/risks.md`, linked to requirements
  threatened and mitigating tests via `Mitigates: RK-NNN` comments. `tools/cli.py
  check-risks` provides mechanical mitigation coverage checking (exit 1 on unmitigated
  risks or orphaned references), mirroring the `SC-NNN` / `check-coverage` pattern.
  `safety-risk-scan` is discovery (per work packet); the catalog is the persistent home
  (promote when S ≥ 8 or systemic). `Risks (RK-NNN)` column added to
  `docs/templates/requirements-traceability-template.md` for bidirectional linkage.
- `risk-catalog` skill, `docs/templates/risk-catalog-template.md`, and
  `.agents/rules/risk-catalog.md` for maintaining the catalog, wiring risks to
  requirements and tests, and enforcing `RK-NNN` ID stability.
- `tests/fixtures/risk-catalog/` three-fixture test suite (`all-covered`, `gap`,
  `orphan`) mirroring the `scenario-traceability` fixture pattern.
- `risk-catalog` added to product feature, product bug, platform migration, and system
  definition skill sequences in `AGENTS.md`.
- Code-driver model woven through the repo: five named drivers (user scenarios, risk, epistemic uncertainty, design intent communication, external obligation) plus a deletion test ("code traceable to no driver is a candidate for removal"). Appears in the `AGENTS.md` shared-understanding contract and behavioral defaults, the `product-brief-template.md` `## Code drivers` section, the `operating-model.md` anti-patterns list, and the `simplify-without-behavior-change` skill's essential-vs-accidental distinction step.
- `docs/adopt-existing-repo.md`, `first-run --mode existing`, and brief-template prompts for preserving existing repo conventions so teams can adopt this workflow incrementally instead of as a greenfield replacement.
- Setup guidance now asks adopters whether Jira ticket IDs should prefix commit messages and pull request titles, and the product-brief and commit templates now record that policy explicitly.
- Repo-wide documentation guidance to avoid historical comments in stable docs and code comments, keeping change history in `CHANGELOG.md`, ADR supersession notes, release notes, and work packets instead.
- `docs/copilot-vscode-playbook.md` and a tracked `.vscode/settings.json` baseline so VS Code adopters get a more concrete Copilot setup path instead of relying only on `.github/copilot-instructions.md`.
- `tools/cli.py doctor` to validate adopter setup across repo files, generated-file sync, Codex, Claude, and Copilot surfaces before first use.
- `tools/cli.py first-run --tool <codex|claude|copilot>` to print a tool-specific happy path with exact next commands and the first recommended prompt.
- README quickstart, golden-path walkthrough, and first-run troubleshooting guidance so adopters can get to a correct first packet with less inference.
- Semantic versioning and changelog policy for this starter repo.
- Durable work-packet structure under `docs/work/<work-id>/` with canonical `brief.md`, `plan.md`, `status.md`, `evidence/`, and `handoffs/`.
- Reusable `work-plan` and `work-status` templates.
- Reusable `bounded-autonomy-loop` skill and loop-log template for fixed-budget Ralph-style execution on narrow, auto-checkable slices.
- Claude-native runtime layer with shared `.claude/settings.json`, starter hooks, path-scoped rules, optional onboarding output style, project-scoped `.mcp.json`, and a Claude playbook.
- Optional `technical-writer` specialist role for release notes, migration guidance, changelog curation, and reader-facing docs.
- Optional `release-manager` and `integration-engineer` specialist roles for release coordination and bench/HIL integration work.
- Reusable `release-readiness` and `lab-and-hil-reproducibility` skills for release gating and real-environment evidence work.
- Optional `workflow-architect` specialist role and reusable `workflow-evolution` skill for evidence-based improvement of prompts, templates, skills, and roles.
- Optional `red-team` specialist role, reusable `plan-red-team` skill, and `docs/templates/red-team-findings-template.md` for adversarial pre-implementation review of `plan.md` on medium/high-risk work before developers begin.
- `product-owner` startup guidance to introduce itself in requester-facing threads and briefly explain how to work through shared understanding before delegation.
- Codex-oriented prompt and config tuning so `product-owner` and `planner` more explicitly favor bounded subagent use when the delegation shape is clear, with `.codex/config.toml` leaving more depth/thread headroom for needed subagents.
- Explicit Codex full-access startup defaults in `.codex/config.toml` (`danger-full-access`, `approval_policy = "never"`) plus repo docs clarifying that Copilot full-access behavior is usually controlled outside the repo.
- Reusable `requirements-and-traceability`, `trade-study-and-decision-analysis`, and `validation-planning` skills plus supporting templates for requirements traceability, trade studies, and validation records.
- C++ embedded design pattern guidance across five firmware skills (`hardware-abstraction`, `simulation-harness-first`, `tdd`, `interface-contract-design`, `resource-budget-review`): policy-based design, CRTP, placement new for MMIO, RAII for peripheral ownership, Active Object test doubles, command queue fakes, ETL containers, HSM dispatch testing, ring buffer/SPSC TDD idiom, table-driven and `std::variant` FSM idioms, observer/event bus contracts, `etl::delegate`, ETL type erasure, memory pool and double-buffer resource checklist items. Includes guardrails for all research-identified gaps (Cortex-M0 atomic ordering, ETL MISRA non-certification, `std::variant` C++17 toolchain caveat, `volatile`+barrier requirement for multi-core/DMA MMIO).
- `story-loop` skill: Ralph-style autonomous loop (pick story → implement → run checks → commit on green → next story); explicitly instantiates `bounded-autonomy-loop` with escalation after 3 consecutive failures. Named after the Ralph Loop (Pocock / snarktank).
- `grill-me` skill: branch-by-branch interrogation for shared-understanding sessions; one question at a time with a recommended answer; reads the codebase instead of asking when possible; covers both brief interrogation (`product-owner`) and plan stress-testing (`planner`).
- `write-a-brief` skill: 5-step guided interview (problem discovery → codebase exploration → requirements interview → module sketch → synthesize) that drives `product-owner` through a shared-understanding session and produces a `docs/work/<id>/brief.md`.
- `design-an-interface` skill: Design It Twice (Ousterhout) implemented as parallel sub-agents with different design constraints (minimize methods / maximize flexibility / optimize common case / ports and adapters); includes firmware-adapted guardrails (ISR-safe, no heap, latency budget).
- `ubiquitous-language` skill: domain glossary extraction; canonical term selection; outputs to `docs/ubiquitous-language.md`; re-runnable with `(updated)` and `(new)` markers.
- `tdd/REFERENCE.md`: extracted embedded-specific TDD idioms (ring buffer / SPSC, table-driven FSM, `std::variant` FSM) as a reference companion to `tdd/SKILL.md`.
- Optional `researcher` specialist role for external domain investigation (datasheets, standards, specs, errata, feasibility signals, technology landscape surveys) when a knowledge gap must be closed before planning is possible.
- Reusable `research` skill that structures external domain investigation into a durable, source-cited research summary and enforces a hard boundary before option comparison or task framing begins.
- `External domain investigation` skill sequence in `AGENTS.md` covering `research` → `planning` → optional `trade-study-and-decision-analysis`.
- Scenario traceability convention: plain-English `SC-NNN` usage scenarios at project (`docs/scenarios.md`) and work-packet (`docs/work/<work-id>/scenarios.md`) level, linked to tests via `Covers: SC-NNN` comments, with a GFM trace table and `tools/cli.py check-coverage` for mechanical gap detection (exit 1 on uncovered scenarios or orphaned references).
- `scenario-traceability` skill: guidance on when to write scenarios, ID format, test reference syntax, trace table, and script usage.
- `docs/templates/scenarios-template.md`: reusable template for scenario files at both scope levels.
- `.agents/rules/` as the canonical source for path-scoped Claude rules, synced to `.claude/rules/` by `tools/cli.py sync`.
- `tools/cli.py`: single-entry-point scaffolding and inspection CLI (stdlib-only, no pip dependencies) with eight subcommands — `new-work`, `new-scenarios`, `new-handoff`, `check-work`, `list-work`, `new-agent`, `new-skill` — plus `sync` (replaces `scripts/sync_agent_layouts.py`) and `check-coverage` (replaces `scripts/check-scenario-coverage.py`). Exit 0 on success, exit 1 on error or gap. Never overwrites existing files.

### Removed

- `scripts/` directory — `scripts/cli.py` has moved to `tools/cli.py` to comply with the Pitchfork C++ layout (`tools/` is the PFL-recognised home for dev tooling).
- `templates/` directory — all 21 template files have moved to `docs/templates/` to comply with the Pitchfork C++ layout (templates are documentation artifacts).
- `scripts/sync_agent_layouts.py` — functionality absorbed into `tools/cli.py sync`.
- `scripts/check-scenario-coverage.py` — functionality absorbed into `tools/cli.py check-coverage`.

### Changed

- The canonical behavior-preserving refactor skill is now named `refactoring`, and the existing-repo onboarding path now uses `doctor --mode existing` so adoption no longer assumes the full starter layout is already present.

- Handoffs now live inside work packets and are expected to be delta records that point back to canonical context files instead of repeating the full brief and plan.
- Bug hypotheses, verification records, and optimization scorecards now fit the shared work-packet structure so durable context stays in one place.
- `release-manager` now treats release shape, explicit gates, artifact identity, and curated release communication as part of the role instead of only version bump and changelog handling.
- `integration-engineer` now treats setup identity, named artifacts, shared-rig discipline, and flaky-environment triage as part of the role instead of only running bench or HIL checks.
- `technical-writer` now treats doc form, recommended task paths, timeless product docs, and accessibility/scannability as part of the role instead of only polishing prose.
- `docs-adr-updates` now captures audience, doc form, timeless durable docs, and accessibility/scannability instead of only stale-doc cleanup and ADR maintenance.
- Planning, interface-contract-design, verification, and the work-packet templates now carry stakeholder context, requirement traceability, trade studies, and validation intent where they matter.
- Flow-inspired refinements now keep design criteria, impact analysis, minimal configuration / exit criteria, and continuous V&V status visible in the normal work-packet flow.
- Workflow evolution now supports bounded experiments under `docs/workflow-experiments/`, with one small mutable surface, explicit evaluation windows, and keep / revise / revert decisions.
- `planner`, `developer`, and the main repo docs now treat bounded autonomous execution as an optional mode with explicit checks, budgets, stop states, and durable loop logs instead of an unbounded retry habit.
- Parallel-lane planning now carries explicit worktree or isolation plans, and Claude-specific workflow improvements are treated as valid workflow-evolution surfaces when the problem is tool-specific.
- `tdd` skill now includes a Step 0 planning phase (confirm interface shape, identify behaviors, surface deep-module opportunities, acknowledge scope); a horizontal-vs-vertical slice anti-pattern diagram; a per-cycle checklist (5 items); and a mocking guardrail (mock at system boundaries only, not at seams inside the unit under test). Embedded-specific idioms moved to the new `REFERENCE.md`.
- `research` skill now requires writing partial findings to the output file within the first 3 tool uses, refining incrementally, so partial results survive context exhaustion.
- `workflow-evolution` skill now documents the Karpathy autoresearch pattern for optimization loops (measurable objective + narrow write surface + auto-check + fixed budget using `bounded-autonomy-loop`); and adds AI-friendly code structure (clear naming, discriminating test names, explicit invariants) as a legitimate hypothesis when a workflow change stalls.
- `AGENTS.md` now includes a three-sentence "why roles" rationale before the Core flow roles list, and a "Skill tiers" section documenting canonical (`.agents/skills/`, synced by `cli.py`), team-installed (`npx skills add`), and personal (global config or gitignored) tiers.
- `docs/operating-model.md` now includes a "Context engineering" section explaining the three layers (project rules files, skills, work packets) and an "Agent failure notes" subsection with a three-field structure (expected / happened / guardrail) filed under `docs/workflow-experiments/`.
- The repo itself now follows the Pitchfork C++ layout it mandates for adopters: `tools/cli.py` (was `scripts/cli.py`), `docs/templates/` (was `templates/`). All canonical `.agents/` sources, top-level docs, `Makefile`, and `README.md` updated to the new paths. Generated files regenerated via `tools/cli.py sync`. `make check-layout` now self-certifies the repo as PFL-compliant.
