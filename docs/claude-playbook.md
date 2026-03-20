# Claude Playbook

This repo includes a concrete Claude Code runtime layer in addition to the shared `.agents/` model.

## Suggested first setup

1. Sign in: `claude auth login`
2. Validate the repo surface: `python3 scripts/cli.py doctor --tool claude`
3. Print the guided first-run sequence: `python3 scripts/cli.py first-run --tool claude`
4. Start Claude in the repo root.
5. Ask: `Use product-owner to summarize the current instructions and available skills, then tell me the next owner and the first durable artifact to create.`

## What is tool-native here

Shared portable workflow logic lives under:

- `.agents/agents/*.toml`
- `.agents/skills/*/SKILL.md`
- `.agents/project/CLAUDE.md`

Claude-native runtime files live under:

- `.claude/settings.json`
- `.claude/rules/`
- `.claude/hooks/`
- `.claude/output-styles/`
- `.mcp.json`

The shared layer stays cross-tool. The Claude-native layer makes that workflow concrete inside Claude Code.

## Project defaults in this starter

[settings.json](/home/sturlalange/Dev/my-claude-skills/.claude/settings.json) makes Claude Code start in a repo-shaped way:

- main thread runs as `product-owner`
- Plan Mode is the shared default
- a small deny list protects obvious secret paths
- hooks are enabled for prompt nudging, compaction continuity, stop quality, and instruction-load logging

If your team wants different local defaults, put them in `.claude/settings.local.json` and keep that file untracked.

## Modular rules

This starter uses `.claude/rules/` for path-scoped runtime guidance rather than one giant extra memory file.

- [agents-and-generation.md](/home/sturlalange/Dev/my-claude-skills/.claude/rules/agents-and-generation.md) narrows generation discipline to canonical and derived agent files
- [docs-and-contract.md](/home/sturlalange/Dev/my-claude-skills/.claude/rules/docs-and-contract.md) narrows SemVer / changelog / durable-doc behavior to contract files
- [claude-runtime.md](/home/sturlalange/Dev/my-claude-skills/.claude/rules/claude-runtime.md) covers Claude-only runtime files such as hooks, settings, output styles, and `.mcp.json`
- [parallel-lanes.md](/home/sturlalange/Dev/my-claude-skills/.claude/rules/parallel-lanes.md) keeps worktree isolation visible when planning parallel lanes

Prefer adding or tightening a path-scoped rule before growing always-loaded instructions.

## Hooks

The starter hooks are documented in [README.md](/home/sturlalange/Dev/my-claude-skills/.claude/hooks/README.md).

They are intentionally bounded:

- `UserPromptSubmit` nudges non-trivial requests toward `product-owner`, work packets, and planner-owned parallelism
- `InstructionsLoaded` logs runtime context under `.claude/logs/`
- `PreCompact` keeps canonical packet pointers alive across compaction
- `SubagentStop` and `Stop` are once-only quality guards for thin closeouts

Treat these as starter guardrails. Tune them from actual usage data.

## Parallel work with worktrees

For parallel write lanes, prefer isolated worktrees when the planner says the split is safe.

- Name the lane, owner, worktree slug, write surface, merge point, and integration checkpoint in `plan.md`
- Keep the active lane and worktree visible in `status.md`
- Keep `.claude/worktrees/` untracked

Typical shape:

```text
lane-a -> .claude/worktrees/<work-id>-lane-a
lane-b -> .claude/worktrees/<work-id>-lane-b
```

Claude Code supports explicit worktree usage from the CLI, so this starter treats worktree isolation as the preferred shape for planner-approved parallel lanes rather than as an ad hoc afterthought.

## Headless and CI-friendly usage

Claude Code also supports headless `-p` usage, which fits verification, review, and report generation.

Examples:

```bash
claude --permission-mode plan -p "Review docs/work/ABC-123/plan.md for missing verification gates."
```

```bash
claude --permission-mode plan --output-format json \
  -p "Use verifier to summarize what is still unverified in docs/work/ABC-123/status.md."
```

Keep headless usage focused on review, planning, verification synthesis, or docs shaping unless your CI environment is intentionally granting broader capabilities.

## MCP

[.mcp.json](/home/sturlalange/Dev/my-claude-skills/.mcp.json) is the project-scoped place for shared MCP server definitions.

Start empty or small. Good first shared servers are usually:

- issue tracker
- docs or spec search
- CI or artifact lookup
- lab or bench management

Do not put raw secrets in `.mcp.json`. Prefer environment variables and repo setup docs.

## Output styles

[repo-onboarding.md](/home/sturlalange/Dev/my-claude-skills/.claude/output-styles/repo-onboarding.md) is an optional example output style.

It is intentionally not the default. Use an output style when you want a different explanation mode, not when you need to change the workflow itself. If you add more styles, keep `keep-coding-instructions: true` unless the style is deliberately non-coding.
