---
paths:
  - ".agents/agents/planner.toml"
  - ".agents/agents/developer.toml"
  - ".agents/skills/planning/SKILL.md"
  - "docs/operating-model.md"
  - "docs/work/**/*.md"
  - "templates/work-plan-template.md"
  - "templates/work-status-template.md"
---

# Parallel Lanes and Worktrees

- When a plan contains parallel write lanes, prefer isolated worktrees or equivalent isolation over one shared dirty tree when the tool supports it.
- Name each lane's owner, write surface, worktree slug or isolation plan, merge point, and integration checkpoint.
- Keep the active worktree or isolation state visible in `status.md` for the current lane.
