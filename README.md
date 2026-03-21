# Agent Skills Starter for Embedded Firmware

A starter repo for a **roles + skills** workflow that works across:

- **Claude Code** project instructions, project skills, and project subagents
- **GitHub Copilot** repository instructions, path-specific instructions, and custom agents
- **OpenAI Codex** project instructions, repo skills, project-scoped config, and custom subagents

Releases of this starter repo aim to follow **Semantic Versioning**, and notable changes are tracked in [CHANGELOG.md](/home/sturlalange/Dev/my-claude-skills/CHANGELOG.md).

## 5-minute quickstart

Pick the tool you want to adopt first, then use the repo CLI to validate the setup before you start tuning prompts or roles.

If you are adopting this into an existing repository instead of starting from this starter layout, see [docs/adopt-existing-repo.md](/home/sturlalange/Dev/my-claude-skills/docs/adopt-existing-repo.md) and use `python3 tools/cli.py first-run --tool <tool> --mode existing`.

### Codex

```bash
npm i -g @openai/codex
codex login
python3 tools/cli.py doctor --tool codex
python3 tools/cli.py first-run --tool codex
```

### Claude Code

```bash
claude auth login
python3 tools/cli.py doctor --tool claude
python3 tools/cli.py first-run --tool claude
```

### GitHub Copilot

Open the repo in your IDE, confirm Copilot is signed in there, then run:

```bash
python3 tools/cli.py doctor --tool copilot
python3 tools/cli.py first-run --tool copilot
```

See [docs/copilot-vscode-playbook.md](/home/sturlalange/Dev/my-claude-skills/docs/copilot-vscode-playbook.md) for the VS Code-specific baseline and workspace settings.

## Golden path

If you want one end-to-end exercise that proves both the repo setup and the operating model:

```bash
python3 tools/cli.py doctor --tool all
python3 tools/cli.py sync
python3 tools/cli.py sync --check
python3 tools/cli.py new-work onboarding-demo
python3 tools/cli.py check-work onboarding-demo
```

Then:

- decide whether Jira ticket IDs should prefix commit messages and PR titles
- fill `docs/work/onboarding-demo/brief.md`
- rerun `python3 tools/cli.py check-work onboarding-demo`
- start your tool and ask `product-owner` to summarize the current instructions and available skills

## Troubleshooting

- `python3 tools/cli.py doctor --tool <tool>` fails on the CLI binary: install that tool and make sure it is on `PATH`
- auth check warns or fails: run `codex login`, `claude auth login`, or verify Copilot sign-in in your IDE
- generated files are out of sync: run `python3 tools/cli.py sync`, then rerun `python3 tools/cli.py sync --check`
- skills or generated agents seem stale: edit canonical files under `.agents/`, not generated files, then rerun `sync`
- Claude hooks or settings do not take effect: confirm the repo is trusted and that `.claude/settings.json` is being loaded
- Copilot behavior does not match the repo: confirm your IDE honors `AGENTS.md`, `.github/copilot-instructions.md`, and `.github/agents/`

This version is biased toward **embedded firmware** and **safety-aware engineering habits**:
- preserve behavior unless intentionally changing it
- prefer simulation before hardware when possible
- keep HAL boundaries explicit
- separate implementation from verification
- treat integration and V&V as continuous signals, not late phases
- track resource and safety risk, not just correctness

## Canonical layout

**`.agents/` is the canonical source of truth** for role definitions and shared skills.

- Canonical role specs live in `.agents/agents/*.toml`
- Canonical shared skills live in `.agents/skills/<skill>/SKILL.md`
- Canonical Claude project instructions live in `.agents/project/CLAUDE.md`
- Generated Claude files live in `.claude/`
- Claude-native runtime defaults live directly under `.claude/` and `.mcp.json`
- Generated Copilot and Codex agent files live in `.github/agents/` and `.codex/agents/`

Run:

```bash
python3 tools/cli.py sync
```

To check for drift without rewriting files:

```bash
python3 tools/cli.py sync --check
```

To validate the local setup before adopting the repo workflow:

```bash
python3 tools/cli.py doctor --tool all
```

To print the exact first-run sequence for one tool:

```bash
python3 tools/cli.py first-run --tool codex
```

For an existing repository adoption path:

```bash
python3 tools/cli.py first-run --tool codex --mode existing
```

## What is included

### Core flow roles
- product-owner
- planner
- developer
- verifier
- reviewer
- firmware-architect

### Optional specialists
- technical-writer
- release-manager
- integration-engineer
- red-team
- researcher
- workflow-architect

### Core skills
- bdd
- codebase-exploration
- planning
- release-readiness
- requirements-and-traceability
- trade-study-and-decision-analysis
- validation-planning
- hypothesis-driven-debugging
- tdd
- bounded-autonomy-loop
- tidy-first
- refactoring
- simplify-without-behavior-change
- verification
- docs-adr-updates
- scenario-traceability
- research
- plan-red-team
- workflow-evolution

### Embedded-specific skills
- interface-contract-design
- hardware-abstraction
- lab-and-hil-reproducibility
- operation-cost-optimization
- simulation-harness-first
- firmware-migration
- safety-risk-scan
- resource-budget-review
- observability-and-diagnostics
- fault-injection-and-recovery

### Reusable templates and prompts
- task, product-brief, work-plan, work-status, requirements-traceability, trade-study, validation, workflow-experiment, bounded-autonomy-loop, handoff, hypothesis, optimization-scorecard, verification, ADR, and git-commit templates under `docs/templates/`
- a starter prompt library in `docs/templates/reusable-prompts.md`

### Embedded build starter
- `extras/cmake-nrf52840-template/`: a concrete CMake firmware starter with checked-in presets, configure-time architecture enforcement, a `gcc-arm-none-eabi` toolchain example, host-side verification, and a minimal nRF52840 hello-world target
- `make check-static-analysis`: repo-owned `clang-tidy` baseline for the CMake starter, intended to be the same command used for local gating and CI
- `.pre-commit-config.yaml` plus `make install-pre-commit`: optional `pre-commit` framework wiring so local commits can run the same static-analysis gate automatically

### Claude-native runtime extras
- `.claude/settings.json` with a repo-level default `product-owner` front door, Plan Mode default, secret-deny starter list, and starter hooks
- `.claude/rules/` for modular path-scoped Claude Code rules
- `.claude/hooks/` for prompt, compaction, and stop guardrails
- `.claude/output-styles/` for optional Claude-only explanation modes that keep coding instructions active
- `.mcp.json` as the project-scoped Claude Code MCP file

### Codex runtime defaults
- `.codex/config.toml` tuned to leave enough depth and thread headroom for bounded specialist delegation when the work benefits from subagents
- `.codex/config.toml` can also set Codex startup sandbox and approval defaults; this repo defaults Codex to `danger-full-access` plus `approval_policy = "never"` for trusted local use

### Startup access defaults
- Claude Code: repo-level `.claude/settings.json` already defaults to `bypassPermissions`
- Codex: repo-level `.codex/config.toml` defaults to `sandbox_mode = "danger-full-access"` and `approval_policy = "never"`
- GitHub Copilot: full-access startup is typically controlled by the user's IDE, extension, or org policy; this repo can document the expectation but does not reliably enforce it from tracked files alone

### Durable work packets

- keep one canonical work packet per non-trivial task under `docs/work/<work-id>/`
- store shared understanding in `brief.md`, execution shape in `plan.md`, and current owner / next action in `status.md`
- store evidence under `docs/work/<work-id>/evidence/`
- store handoffs under `docs/work/<work-id>/handoffs/` as delta records that point back to the canonical packet files
- keep lightweight continuous V&V status in `status.md` so verification, validation, and integration gaps stay visible during iteration
- store bounded process-improvement experiments under `docs/workflow-experiments/`
- keep work packets out of top-level architecture docs so the docs tree stays non-intrusive

### Git commit rules

- prefer one logical change per commit
- commit when one logical change has reached a stable, reviewable, verified checkpoint
- switch tidy, refactor, and behavioral work between commits rather than mixing them
- use patch or interactive staging when needed to keep commits atomic
- before changing direction, commit the stable slice or discard it instead of carrying half-finished state forward
- prefer Conventional Commit style subjects like `fix(storage): avoid redundant flash erase`
- keep the subject short, imperative, and without a trailing period
- add a body when the why, tradeoffs, or alternatives are not obvious
- use `BREAKING CHANGE:`, `Co-authored-by:`, or `Signed-off-by:` trailers only when relevant or required

### Semantic versioning and changelog

- published releases of this repo aim to follow Semantic Versioning
- treat the documented repo contract as the public API: canonical `.agents/` paths, generated layout expectations, role names, skill names, template names, and documented workflow conventions
- bump `MAJOR` for breaking changes to that contract
- bump `MINOR` for backward-compatible additions
- bump `PATCH` for backward-compatible fixes and clarifications
- once a version is released, treat it as immutable and publish a new version for later changes instead of rewriting the old one
- keep a curated root [CHANGELOG.md](/home/sturlalange/Dev/my-claude-skills/CHANGELOG.md) with an `Unreleased` section
- let generated release notes assist if useful, but keep the changelog human-curated
- group changelog entries under headings like `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`

### Control flow

For non-trivial work, the intended front door is `product-owner`: you align on the problem, scope, non-goals, constraints, acceptance criteria, and any public-contract or release impact first, write the canonical brief into the work packet, then `product-owner` delegates to the right specialist or planned specialist set. `planner` should identify safe parallel lanes when work can be split cleanly, maintain the canonical plan, and carry forward the SemVer / changelog implication when the documented contract changes. When the current execution slice is narrow, auto-checkable, and has explicit stop conditions, `planner` may recommend `bounded-autonomy-loop` as an execution mode instead of inventing a new owner. When reader-facing docs, release notes, migration guidance, or doc-structure cleanup become their own substantial lane, delegate that lane to `technical-writer`. When release readiness, version-bump synthesis, release shape, or final release communication become their own lane, delegate to `release-manager`. When bench, HIL, flashing, integration-environment setup, or flaky-lab triage become their own lane, delegate to `integration-engineer`. When repeated workflow friction or missing reusable guidance becomes its own lane, delegate to `workflow-architect`. Use the work packet to keep intent, design criteria, impact analysis, minimal configurations, exit criteria, and continuous V&V status visible as the work evolves. For process changes, prefer bounded experiments in `docs/workflow-experiments/` with one small mutable surface and an explicit keep / revise / revert decision.

### Claude Code runtime

- use `.claude/settings.json` for team-shared Claude defaults, and `.claude/settings.local.json` for personal overrides
- keep shared workflow logic in `.agents/`, and Claude-only runtime behavior in `.claude/` plus `.mcp.json`
- prefer path-scoped `.claude/rules/` files over one giant extra memory file
- use the starter hooks to preserve work-packet continuity and closeout quality, then tune them from real usage
- prefer isolated worktrees for planner-approved parallel write lanes and keep the lane + worktree visible in `status.md`
- use headless `claude -p` flows for planning, review, verification synthesis, and CI-friendly reporting when that helps

### Bounded autonomous execution

- use `bounded-autonomy-loop` only for a narrow slice with explicit done-when criteria
- define the objective, allowed write surface, checks per iteration, and fixed budget before the loop starts
- keep a durable loop record under `docs/work/<work-id>/evidence/bounded-autonomy-loop.md`
- stop on `complete`, `blocked`, or `budget exhausted`
- do not use it for ambiguous design work, unknown-cause debugging, or flaky hardware loops

### Preferred testing strategy

- use `bdd` to define behavior and acceptance scenarios
- use `tdd` as the implementation loop for product development
- prefer the test pyramid
- prefer `simulation-harness-first` before hardware-only checks when practical
- non-productized tools may skip `tdd` when the plan says so explicitly and still defines verification

### Preferred optimization strategy

- use `operation-cost-optimization` when performance, endurance, churn, RAM pressure, or flash pressure matters
- count expensive indirect operations behind a seam, or measure direct RAM/flash footprint explicitly
- assign explicit weights when they help rank tradeoffs instead of guessing
- prove the required behavior still holds after the optimization

## Layout

```text
. 
├── CHANGELOG.md
├── .mcp.json
├── AGENTS.md
├── README.md
├── .agents/
│   ├── agents/
│   │   └── <role>.toml
│   ├── project/
│   │   └── CLAUDE.md
│   └── skills/
│       └── <skill-name>/SKILL.md
├── .claude/
│   ├── CLAUDE.md                  # generated
│   ├── settings.json              # Claude-native runtime defaults
│   ├── hooks/
│   │   └── *.py
│   ├── output-styles/
│   │   └── *.md
│   ├── rules/
│   │   └── *.md
│   ├── agents/                    # generated
│   │   ├── developer.md
│   │   ├── firmware-architect.md
│   │   ├── integration-engineer.md
│   │   ├── planner.md
│   │   ├── product-owner.md
│   │   ├── release-manager.md
│   │   ├── reviewer.md
│   │   ├── technical-writer.md
│   │   ├── workflow-architect.md
│   │   └── verifier.md
│   └── skills/                    # generated from .agents/skills
│       └── <skill-name>/SKILL.md
├── .codex/
│   ├── config.toml
│   └── agents/                    # generated
│       ├── developer.toml
│       ├── firmware-architect.toml
│       ├── integration-engineer.toml
│       ├── planner.toml
│       ├── product-owner.toml
│       ├── release-manager.toml
│       ├── reviewer.toml
│       ├── technical-writer.toml
│       ├── workflow-architect.toml
│       └── verifier.toml
├── .github/
│   ├── copilot-instructions.md
│   ├── agents/                    # generated
│   │   ├── developer.agent.md
│   │   ├── firmware-architect.agent.md
│   │   ├── integration-engineer.agent.md
│   │   ├── planner.agent.md
│   │   ├── product-owner.agent.md
│   │   ├── release-manager.agent.md
│   │   ├── reviewer.agent.md
│   │   ├── technical-writer.agent.md
│   │   ├── workflow-architect.agent.md
│   │   └── verifier.agent.md
│   └── instructions/
│       ├── build-system.instructions.md
│       ├── docs.instructions.md
│       ├── firmware.instructions.md
│       └── tests.instructions.md
├── docs/
│   ├── claude-playbook.md
│   ├── codex-playbook.md
│   ├── compatibility.md
│   ├── firmware-playbook.md
│   ├── templates/
│   │   ├── adr-template.md
│   │   ├── bug-report-template.md
│   │   ├── codex-global-agents-template.md
│   │   ├── git-commit-template.txt
│   │   ├── handoff-template.md
│   │   ├── hypothesis-template.md
│   │   ├── optimization-scorecard-template.md
│   │   ├── product-brief-template.md
│   │   ├── reusable-prompts.md
│   │   ├── task-template.md
│   │   ├── work-plan-template.md
│   │   ├── work-status-template.md
│   │   └── verification-template.md
│   ├── work/
│   │   └── README.md
│   └── operating-model.md
├── extras/
│   └── cmake-nrf52840-template/
│       ├── CMakeLists.txt
│       ├── CMakePresets.json
│       ├── cmake/
│       ├── ld/
│       ├── libs/
│       ├── src/
│       └── tests/
└── tools/
    └── cli.py
```

## How to customize it

1. Edit the canonical files under `.agents/` first.
2. Run `python3 tools/cli.py sync`.
3. Replace placeholder build/test commands in `.agents/project/CLAUDE.md`.
4. Tune `.claude/settings.json`, `.claude/rules/`, `.claude/hooks/`, and `.mcp.json` to match your team's Claude workflow.
5. Tune `.codex/config.toml` for your sandbox, approval, and role preferences.
6. Tighten `.github/instructions/*.instructions.md` to match your stack:
   - Zephyr / West
   - CMake Presets
   - Unity / CppUTest / GoogleTest
   - host simulation harnesses
   - hardware integration tests
7. Start from `extras/cmake-nrf52840-template/` when you want a concrete embedded CMake baseline instead of inventing one from scratch.
8. Add project-specific architecture constraints in `docs/firmware-playbook.md`.
9. Keep `AGENTS.md` short and stable. Put detailed guidance in skills, Claude rules, hooks, and path-specific instructions.
10. Reuse and adapt prompts from `docs/templates/reusable-prompts.md` instead of rewriting task prompts from scratch.
11. Store durable task context under `docs/work/<work-id>/` instead of scattering it across chat and repeated handoff summaries.
12. Optionally set a commit template with `git config commit.template docs/templates/git-commit-template.txt`.
13. Keep `CHANGELOG.md` current for notable unreleased changes and choose the SemVer bump deliberately at release time.
14. Keep CI workflow YAML thin. Put substantive setup and check logic in repo-tracked scripts or Make targets under `tools/`, then call those entrypoints from GitHub Actions.
15. Prefer Python over Bash for repo-owned automation once the logic grows beyond a short shell wrapper. Keep shell for small wrappers around package installs or linear command sequences.

## Suggested firmware workflow

Start with `product-owner` to create a shared brief, then use the following skill sequences.

Bring in `technical-writer` when release notes, migration guides, deprecation communication, changelog curation, doc-structure cleanup, or other reader-facing docs deserve a dedicated owner instead of being folded into the implementation lane.
Bring in `release-manager` when version bump, changelog finalization, release shape, release readiness, or final release communication deserve a dedicated owner.
Bring in `integration-engineer` when HIL, flashing, bench repro, integration-environment work, or flaky-lab triage becomes its own substantial lane.
Bring in `workflow-architect` when repeated workflow friction, unclear role boundaries, or a likely new prompt, template, skill, or role deserves its own lane.
Use `bounded-autonomy-loop` only when the current execution slice is narrow, auto-checkable, and has an explicit budget plus stop conditions.
When parallel lanes are approved, prefer isolated worktrees and keep lane names plus worktree slugs visible in `plan.md` and `status.md`.

### Product feature
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

### Product bug fix
1. `codebase-exploration`
2. `hypothesis-driven-debugging`
3. `requirements-and-traceability` when expected behavior or ownership is unclear
4. `bdd`
5. `simulation-harness-first`
6. `tdd`
7. `verification`
8. `fault-injection-and-recovery`
9. `docs-adr-updates` if the design truth changed

For bug work, keep a durable debug trail under `docs/work/<work-id>/evidence/hypotheses/` with one file per hypothesis.

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
4. `tdd` only when the tool is expected to become shared, long-lived, or high-risk
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

### Platform migration
1. `codebase-exploration`
2. `planning`
3. `firmware-migration`
4. `hardware-abstraction`
5. `simulation-harness-first`
6. `verification`
7. `safety-risk-scan`
8. `resource-budget-review`

## Design philosophy

- **roles over personalities**
- **product-owner before delegation**
- **skills over giant prompts**
- **one canonical source under `.agents/`**
- **remove before add**
- **prove before claiming**
- **prefer reversible paths**
- **say what was not verified**
