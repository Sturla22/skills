# Agent Skills Starter for Embedded Firmware

A starter repo for a **roles + skills** workflow that works across:

- **Claude Code** project instructions, project skills, and project subagents
- **GitHub Copilot** repository instructions, path-specific instructions, and custom agents
- **OpenAI Codex** project instructions, repo skills, project-scoped config, and custom subagents

This version is biased toward **embedded firmware** and **medical / safety-aware engineering habits**:
- preserve behavior unless intentionally changing it
- prefer simulation before hardware when possible
- keep HAL boundaries explicit
- separate implementation from verification
- track resource and safety risk, not just correctness

## What changed in this variant

This version makes **`.agents/` the canonical source of truth** for role definitions and shared skills.

- Canonical role specs live in `.agents/agents/*.toml`
- Canonical shared skills live in `.agents/skills/<skill>/SKILL.md`
- Canonical Claude project instructions live in `.agents/project/CLAUDE.md`
- Generated Claude files live in `.claude/`
- Generated Copilot and Codex agent files live in `.github/agents/` and `.codex/agents/`

Run:

```bash
python3 scripts/sync_agent_layouts.py
```

To check for drift without rewriting files:

```bash
python3 scripts/sync_agent_layouts.py --check
```

## What is included

### Core roles
- planner
- developer
- verifier
- reviewer
- firmware-architect

### Core skills
- codebase-exploration
- planning
- hypothesis-driven-debugging
- tdd
- tidy-first
- refactoring
- simplify-without-behavior-change
- verification
- docs-adr-updates

### Embedded-specific skills
- interface-contract-design
- hardware-abstraction
- simulation-harness-first
- firmware-migration
- safety-risk-scan
- resource-budget-review
- observability-and-diagnostics
- fault-injection-and-recovery

## Layout

```text
.
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
│   ├── agents/                    # generated
│   │   ├── developer.md
│   │   ├── firmware-architect.md
│   │   ├── planner.md
│   │   ├── reviewer.md
│   │   └── verifier.md
│   └── skills/                    # generated from .agents/skills
│       └── <skill-name>/SKILL.md
├── .codex/
│   ├── config.toml
│   └── agents/                    # generated
│       ├── developer.toml
│       ├── firmware-architect.toml
│       ├── planner.toml
│       ├── reviewer.toml
│       └── verifier.toml
├── .github/
│   ├── copilot-instructions.md
│   ├── agents/                    # generated
│   │   ├── developer.agent.md
│   │   ├── firmware-architect.agent.md
│   │   ├── planner.agent.md
│   │   ├── reviewer.agent.md
│   │   └── verifier.agent.md
│   └── instructions/
│       ├── build-system.instructions.md
│       ├── docs.instructions.md
│       ├── firmware.instructions.md
│       └── tests.instructions.md
├── docs/
│   ├── codex-playbook.md
│   ├── compatibility.md
│   ├── firmware-playbook.md
│   └── operating-model.md
├── scripts/
│   └── sync_agent_layouts.py
└── templates/
    ├── adr-template.md
    ├── bug-report-template.md
    ├── codex-global-agents-template.md
    ├── handoff-template.md
    ├── task-template.md
    └── verification-template.md
```

## How to customize it

1. Edit the canonical files under `.agents/` first.
2. Run `python3 scripts/sync_agent_layouts.py`.
3. Replace placeholder build/test commands in `.agents/project/CLAUDE.md`.
4. Tune `.codex/config.toml` for your sandbox, approval, and role preferences.
5. Tighten `.github/instructions/*.instructions.md` to match your stack:
   - Zephyr / West
   - CMake Presets
   - Unity / CppUTest / GoogleTest
   - host simulation harnesses
   - hardware integration tests
6. Add project-specific architecture constraints in `docs/firmware-playbook.md`.
7. Keep `AGENTS.md` short and stable. Put detailed guidance in skills and path-specific instructions.

## Suggested firmware workflow

### New feature
1. `codebase-exploration`
2. `planning`
3. `interface-contract-design`
4. `simulation-harness-first`
5. `tdd`
6. implementation
7. `verification`
8. `resource-budget-review`
9. `docs-adr-updates`

### Bug fix
1. `codebase-exploration`
2. `hypothesis-driven-debugging`
3. `simulation-harness-first`
4. `tdd`
5. `verification`
6. `fault-injection-and-recovery`
7. `docs-adr-updates` if the design truth changed

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
- **skills over giant prompts**
- **one canonical source under `.agents/`**
- **remove before add**
- **prove before claiming**
- **prefer reversible paths**
- **say what was not verified**
