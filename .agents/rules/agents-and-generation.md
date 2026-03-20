---
paths:
  - ".agents/**/*.toml"
  - ".agents/**/*.md"
  - ".claude/agents/**/*.md"
  - ".claude/skills/**/*.md"
  - ".claude/rules/**/*.md"
  - ".github/agents/**/*.md"
  - ".codex/agents/**/*.toml"
  - "scripts/cli.py"
---

# Canonical Roles and Skills

- Edit shared role definitions under `.agents/agents/*.toml`.
- Edit shared skills under `.agents/skills/*/SKILL.md`.
- Edit shared rules under `.agents/rules/*.md`.
- Treat `.claude/agents/`, `.claude/skills/`, `.claude/rules/`, `.github/agents/`, and `.codex/agents/` as generated outputs unless the task is explicitly about generation behavior.
- Run `python3 scripts/cli.py sync` after canonical changes and `python3 scripts/cli.py sync --check` before declaring the generated layers in sync.
- If generated output is wrong, fix the canonical source or the generator instead of hand-patching the derived copy.
