# Research: copilot default agent

**Research question:** Does GitHub Copilot support a repo-level default custom agent selection, and can this repository make `product-owner` the default Copilot agent in a runtime-enforced way rather than only through instructions?
**Retrieval date:** 2026-03-25

## Key findings
| Finding | Source | Version | Section |
|---------|--------|---------|---------|
| Claude has an explicit runtime default in this repo via `.claude/settings.json` with `"agent": "product-owner"`. This is repo-local evidence of a real default-agent knob on the Claude side. | `C:\Users\slange\Dev\skills\.claude\settings.json` | working tree | lines 1-8 |
| Repo-local sync logic generates Copilot agent files under `.github/agents/*.agent.md` from canonical `.agents/agents/*.toml`, but there is no analogous Copilot repo config in this repo that sets a default selected agent. | `C:\Users\slange\Dev\skills\tools\cli.py` | working tree | lines 598-610 |
| Copilot CLI officially documents three ways to use custom agents: `/agent`, explicit prompt instruction, and `copilot --agent ... --prompt ...`. This is documented agent selection, not a repo-level default-selection setting. | GitHub Docs: “Creating and using custom agents for GitHub Copilot CLI” | web page at retrieval | “Using a custom agent” |
| Copilot CLI also documents inference: when you prompt Copilot, it may choose to use one of your custom agents if it determines the agent is a good fit for the task. | GitHub Docs: “Creating and using custom agents for GitHub Copilot CLI” | web page at retrieval | “Introduction”; “Using a custom agent” → “By inference” |
| The custom-agent reference documents `disable-model-invocation`. When `true`, Copilot will not automatically use the custom agent based on task context and the agent must be manually selected. If unset, it defaults to `false`. | GitHub Docs: “Custom agents configuration” | web page at retrieval | “YAML frontmatter properties” |
| The same reference documents `user-invocable`. When `false`, the custom agent cannot be manually selected and can only be accessed programmatically. | GitHub Docs: “Custom agents configuration” | web page at retrieval | “YAML frontmatter properties” |
| Copilot CLI docs describe repository-wide instructions (`.github/copilot-instructions.md`), path-specific instructions, and `AGENTS.md` as automatically included context. This supports behavior shaping, but it is distinct from a documented default custom-agent selector. | GitHub Docs: “Using GitHub Copilot CLI” | web page at retrieval | “Use custom instructions” |
| GitHub’s coding-agent management docs describe choosing an agent from a dropdown when starting a task. This again documents manual selection at task start, not a repository setting that preselects one custom agent for all sessions. | GitHub Docs: “Managing coding agents” | web page at retrieval | “1. Select a repository and choose your agent” |

## Gaps and open items
- No authoritative Copilot document was found that explicitly says “you cannot set a repo-level default custom agent.” The current conclusion is therefore based on positive documentation of supported mechanisms plus absence of a documented repo setting in the fetched primary sources.
- No authoritative source was found that shows `/agent` selection persisting per repository across sessions.
- It remains possible that an undocumented or newly released feature exists outside the fetched docs; none was found in the official pages reviewed here.

## Research boundary
Facts established above. Design options and trade-offs begin here — hand to planner.
