# Codex Playbook

This repo includes Codex-native project files in addition to the Claude Code and GitHub Copilot files.

## What is included

- `AGENTS.md` at repo root for durable project guidance
- `.agents/skills/` for shared repo skills that Codex can discover automatically
- `.agents/agents/*.toml` as the canonical role specs
- `.codex/config.toml` for project-scoped Codex settings
- `.codex/agents/*.toml` as generated Codex subagents

## Why the repo has both `.agents` and `.codex/agents`

- `.agents/skills` is the Codex repo skill location.
- `.agents/agents/*.toml` is the canonical shared role layer.
- `.codex/agents/*.toml` is generated so Codex subagent config stays tool-native.
- `.claude/` and `.github/agents/` are generated from the same canonical role definitions.

## Suggested first setup

1. Install Codex CLI: `npm i -g @openai/codex`
2. Run `codex` in the repo root and sign in.
3. Ask Codex: `Summarize the current instructions and available skills.`
4. Open `.codex/config.toml` and tune approvals, sandboxing, and any model defaults.
5. Decide whether your team will run mostly in the CLI, the IDE extension, or the Codex app.

## Regenerating role files

Whenever you edit `.agents/agents/*.toml`, run:

```bash
python3 scripts/sync_agent_layouts.py
```

To enforce this in CI:

```bash
python3 scripts/sync_agent_layouts.py --check
```

## Quick checks

### Instruction loading
Run from the repo root:

```bash
codex --ask-for-approval never "Summarize the current instructions."
```

### Skill discovery
From the repo root, ask Codex to list skills or invoke one explicitly using the skill name.
Examples:

```text
Use codebase-exploration to map the files involved in the boot sequence.
Use hypothesis-driven-debugging to investigate this flaky integration test.
Use simplify-without-behavior-change on this storage adapter.
```

### Subagent usage
Custom agents live in `.codex/agents/` and mirror the repo role model.
Examples:

- planner: framing, scope, acceptance criteria
- developer: minimal implementation
- verifier: proof and focused checks
- reviewer: adversarial critique
- firmware-architect: contracts and boundaries

## Embedded-firmware defaults worth keeping

- Keep `AGENTS.md` short and durable.
- Put repeatable workflows into skills, not giant prompts.
- Bias toward simulation and host verification before hardware-only work when practical.
- Treat resource use and failure behavior as part of correctness.
- Keep migration decisions and interface constraints documented.

## Good Codex prompts for this repo

### Feature planning
"Use the planner to scope this change, list affected modules, and define verification steps before any edits."

### Small implementation
"Use developer to make the smallest defensible change for this bug, then hand off to verifier."

### Adversarial review
"Have reviewer critique this patch for correctness, complexity, and missing evidence."

### Migration work
"Use firmware-architect and planner to propose an incremental migration path with characterization checkpoints."
