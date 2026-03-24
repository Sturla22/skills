# AI for Firmware Engineers — Össur R&D Bionics

**From Copilot → Skills → Agent Systems** · 9-session series

---

## Core Thesis

We are moving from **writing code** to **designing systems that produce code**.

```
Prompt → Skill → Agent → Agent System
```

> “Skills are your HAL for AI.”

---

## Session Arc

| # | Session | Key Shift | Nugget |
|---|---------|-----------|--------|
| 1 | **Copilot** | AI as context-aware autocomplete | “Nudge, don’t outsource” |
| 2 | **Prompting & Roles** | Autocomplete → directing behavior | “Prompts are specifications, not questions” |
| 3 | **Skills** ⚡ | One-off prompt → reusable capability | “If you use a prompt twice, make it a skill” |
| 4 | **CLI & Automation** | Chat → workflow integration | “If it’s text, it’s automatable” |
| 5 | **Context Engineering** | More context → right context | “Curate, don’t dump” |
| 6 | **Debugging with AI** | AI as hypothesis generator | “Logs are gold” |
| 7 | **Agents** | Single answer → structured loop | “Agent = Skill + Process + Loop” |
| 8 | **Agent Teams** | One agent → specialized roles | “One agent, one responsibility” |
| 9 | **Systems Thinking** | Writing code → orchestrating work | “You are not writing code — you are designing systems of work” |

---

## The Inflection Point — Skills

A skill is a **reusable, structured capability** that encodes how we think, not just what we do.

```markdown
# SKILL: Firmware Code Review
Role: Senior embedded firmware engineer
Inputs: code, platform, constraints
Process: check memory safety → concurrency → edge cases
Output: issues + fixes
```

Skills give AI your engineering context. Without them, AI is generic. With them, AI understands your platform, your rules, your workflow.

---

## Real Example — Össur

Two skills wired together into a live development loop:

- **Bitbucket Skill** — agent creates PRs, comments, reads pipeline results
- **B3C Migration Skill** — encodes architecture rules and migration patterns

```
Code change → PR → CI pipeline → Agent reads results → Agent suggests fixes → PR updated
```

> “The agent is now part of the development lifecycle — not a chat window.”

---

## The 12 Rules

1. Give the agent a role · 2. Add constraints · 3. Keep tasks small · 4. Ask for process
5. Use CLI · 6. Build skills · 7. Reuse everything · 8. Verify outputs
9. Think in loops · 10. Use specialized agents · 11. Context matters most · 12. Design systems, not prompts

---

## Closing

> “We are not just using AI — we are extending it with our engineering system.”

> “In a year, writing firmware without AI will feel like writing C without a compiler.”
