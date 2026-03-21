# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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
- The repo itself now follows the Pitchfork C++ layout it mandates for adopters: `tools/cli.py` (was `scripts/cli.py`), `docs/templates/` (was `templates/`). All canonical `.agents/` sources, top-level docs, `Makefile`, and `README.md` updated to the new paths. Generated files regenerated via `tools/cli.py sync`. `make check-layout` now self-certifies the repo as PFL-compliant.
