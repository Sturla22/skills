# Compatibility Notes

## Canonical source of truth

This repo treats `.agents/` as canonical.

- `.agents/agents/*.toml` defines the shared role model
- `.agents/skills/<skill-name>/SKILL.md` defines shared skills
- `.agents/project/CLAUDE.md` defines Claude project instructions

Run `python3 scripts/cli.py sync` after editing canonical agent or skill files.

## Claude Code

Generated Claude Code files live in:

- `.claude/CLAUDE.md`
- `.claude/skills/<skill-name>/SKILL.md`
- `.claude/agents/*.md`

Claude-native runtime files can also live alongside the generated layer:

- `.claude/settings.json`
- `.claude/rules/`
- `.claude/hooks/`
- `.claude/output-styles/`
- `.mcp.json`

Claude-specific discovery stays native, but the shared role and skill content comes from `.agents/`.
Treat the runtime files above as Claude-only overlays for settings, hooks, rules, output styles, and shared MCP servers; they are not generated from `.agents/`.

## GitHub Copilot

This repo uses GitHub Copilot customization layers:

- `.github/copilot-instructions.md` for repository-wide instructions
- `.github/instructions/*.instructions.md` for path-specific instructions
- `.github/agents/*.agent.md` for custom agents
- `AGENTS.md` as a repo-level agent instruction file
- `.vscode/settings.json` for a workspace baseline that points Copilot features at the repo guidance when adopters use VS Code

The custom agent files under `.github/agents/` are generated from `.agents/agents/*.toml`.

## OpenAI Codex

This repo uses Codex-native project layers:

- `AGENTS.md` for root project instructions
- `.agents/skills/<skill-name>/SKILL.md` for shared repo skills
- `.codex/config.toml` for project-scoped Codex configuration
- `.codex/agents/*.toml` for custom Codex subagents

The custom agent files under `.codex/agents/` are generated from `.agents/agents/*.toml`.

## Why all three are present

The goal is not to make one giant shared prompt. Instead:

- `AGENTS.md` stays short and durable
- `.agents/` is the portable shared layer
- the shared role model can start with `product-owner` regardless of tool
- `.claude/` stays compatible with Claude Code discovery
- `.claude/settings.json`, `.claude/rules/`, `.claude/hooks/`, `.claude/output-styles/`, and `.mcp.json` make Claude Code behavior concrete without forcing those mechanics on Codex or Copilot
- `.github/agents/` stays compatible with Copilot custom agents
- `.vscode/settings.json` gives VS Code adopters a repo-tracked baseline for Copilot features such as code generation, review, commit-message generation, and PR-description generation
- `.codex/agents/` stays compatible with Codex subagents
- `.github/instructions/` adds path-specific guidance that does not belong in shared role files

## Suggested adaptation strategy

- Start by validating the repo surface with `python3 scripts/cli.py doctor --tool all`.
- Use `python3 scripts/cli.py first-run --tool codex`, `--tool claude`, or `--tool copilot` to give adopters one exact happy path per tool.
- Then customize `AGENTS.md`, `.agents/project/CLAUDE.md`, `.claude/settings.json`, and `.github/copilot-instructions.md`.
- After that, tune `.claude/rules/`, `.claude/hooks/`, `.mcp.json`, and `.codex/config.toml`.
- Only after that, tune skills and path-specific instructions to match your build, test, and firmware boundaries.
- Use `python3 scripts/cli.py sync --check` in CI to catch drift.
