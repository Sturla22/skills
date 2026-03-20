---
paths:
  - "AGENTS.md"
  - "README.md"
  - "CHANGELOG.md"
  - "docs/**/*.md"
  - "templates/**/*.md"
---

# Docs and Contract Files

- This repo's documented workflow is part of the public contract, so compatibility, SemVer, and changelog implications matter when docs or templates change.
- Keep durable work-packet paths, handoff paths, and evidence paths consistent across docs.
- Prefer concise, stable guidance over transcript-like narration or duplicated context.
- Prefer current-state wording over historical commentary in stable docs; keep history in `CHANGELOG.md`, ADR supersession notes, release notes, or work packets.
- When a Claude-only artifact changes the documented workflow, explain that it is tool-specific rather than silently implying all tools behave the same way.
