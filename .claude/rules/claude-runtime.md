---
paths:
  - ".claude/**/*.json"
  - ".claude/hooks/**/*"
  - ".claude/output-styles/**/*"
  - ".claude/rules/**/*"
  - ".mcp.json"
---

# Claude Runtime Files

- Keep shared, portable role and skill logic in `.agents/`; use `.claude/` and `.mcp.json` only for Claude-specific runtime behavior.
- Treat `.claude/settings.json` as team-shared defaults and `.claude/settings.local.json` as personal override space.
- Keep hooks safe, bounded, and observable. Prefer advisory or once-only blocking behavior over hard-to-escape loops.
- Prefer path-scoped rules to giant always-loaded instruction files.
- If you add an output style, keep `keep-coding-instructions: true` unless the style is intentionally non-coding.
- Do not store secrets directly in `.mcp.json`; prefer environment variables and documented setup.
