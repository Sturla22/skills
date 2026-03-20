# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Semantic versioning and changelog policy for this starter repo.
- Durable work-packet structure under `docs/work/<work-id>/` with canonical `brief.md`, `plan.md`, `status.md`, `evidence/`, and `handoffs/`.
- Reusable `work-plan` and `work-status` templates.
- Reusable `bounded-autonomy-loop` skill and loop-log template for fixed-budget Ralph-style execution on narrow, auto-checkable slices.
- Claude-native runtime layer with shared `.claude/settings.json`, starter hooks, path-scoped rules, optional onboarding output style, project-scoped `.mcp.json`, and a Claude playbook.
- Optional `technical-writer` specialist role for release notes, migration guidance, changelog curation, and reader-facing docs.
- Optional `release-manager` and `integration-engineer` specialist roles for release coordination and bench/HIL integration work.
- Reusable `release-readiness` and `lab-and-hil-reproducibility` skills for release gating and real-environment evidence work.
- Optional `workflow-architect` specialist role and reusable `workflow-evolution` skill for evidence-based improvement of prompts, templates, skills, and roles.
- Optional `red-team` specialist role, reusable `plan-red-team` skill, and `templates/red-team-findings-template.md` for adversarial pre-implementation review of `plan.md` on medium/high-risk work before developers begin.
- `product-owner` startup guidance to introduce itself in requester-facing threads and briefly explain how to work through shared understanding before delegation.
- Reusable `requirements-and-traceability`, `trade-study-and-decision-analysis`, and `validation-planning` skills plus supporting templates for requirements traceability, trade studies, and validation records.
- C++ embedded design pattern guidance across five firmware skills (`hardware-abstraction`, `simulation-harness-first`, `tdd`, `interface-contract-design`, `resource-budget-review`): policy-based design, CRTP, placement new for MMIO, RAII for peripheral ownership, Active Object test doubles, command queue fakes, ETL containers, HSM dispatch testing, ring buffer/SPSC TDD idiom, table-driven and `std::variant` FSM idioms, observer/event bus contracts, `etl::delegate`, ETL type erasure, memory pool and double-buffer resource checklist items. Includes guardrails for all research-identified gaps (Cortex-M0 atomic ordering, ETL MISRA non-certification, `std::variant` C++17 toolchain caveat, `volatile`+barrier requirement for multi-core/DMA MMIO).
- Optional `researcher` specialist role for external domain investigation (datasheets, standards, specs, errata, feasibility signals, technology landscape surveys) when a knowledge gap must be closed before planning is possible.
- Reusable `research` skill that structures external domain investigation into a durable, source-cited research summary and enforces a hard boundary before option comparison or task framing begins.
- `External domain investigation` skill sequence in `AGENTS.md` covering `research` → `planning` → optional `trade-study-and-decision-analysis`.
- Scenario traceability convention: plain-English `SC-NNN` usage scenarios at project (`docs/scenarios.md`) and work-packet (`docs/work/<work-id>/scenarios.md`) level, linked to tests via `Covers: SC-NNN` comments, with a GFM trace table and `scripts/cli.py check-coverage` for mechanical gap detection (exit 1 on uncovered scenarios or orphaned references).
- `scenario-traceability` skill: guidance on when to write scenarios, ID format, test reference syntax, trace table, and script usage.
- `templates/scenarios-template.md`: reusable template for scenario files at both scope levels.
- `.agents/rules/` as the canonical source for path-scoped Claude rules, synced to `.claude/rules/` by `scripts/cli.py sync`.
- `scripts/cli.py`: single-entry-point scaffolding and inspection CLI (stdlib-only, no pip dependencies) with eight subcommands — `new-work`, `new-scenarios`, `new-handoff`, `check-work`, `list-work`, `new-agent`, `new-skill` — plus `sync` (replaces `scripts/sync_agent_layouts.py`) and `check-coverage` (replaces `scripts/check-scenario-coverage.py`). Exit 0 on success, exit 1 on error or gap. Never overwrites existing files.

### Removed

- `scripts/sync_agent_layouts.py` — functionality absorbed into `scripts/cli.py sync`.
- `scripts/check-scenario-coverage.py` — functionality absorbed into `scripts/cli.py check-coverage`.

### Changed

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
