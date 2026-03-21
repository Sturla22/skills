# Copilot VS Code Playbook

This repo can shape GitHub Copilot in VS Code, but it cannot enforce runtime behavior as completely as Claude Code or Codex.

## What the repo can control

- `AGENTS.md` for the shared operating model
- `.github/copilot-instructions.md` for repository-wide Copilot guidance
- `.github/instructions/*.instructions.md` for path-specific guidance
- `.github/agents/*.agent.md` for custom agents
- `.vscode/settings.json` for a workspace baseline that points Copilot features at the repo instructions

## What still lives in the adopter's IDE or account

- GitHub sign-in and Copilot entitlement
- model selection and any user-level preferences
- which VS Code extensions are installed and enabled
- whether personal or organization instructions override repo guidance

## Suggested first setup

1. Install or update the GitHub Copilot and GitHub Copilot Chat extensions in VS Code.
2. Sign in to GitHub from VS Code and confirm Copilot is active.
3. Open this repository as the workspace root.
4. Run `python3 tools/cli.py doctor --tool copilot`.
5. Run `python3 tools/cli.py first-run --tool copilot`.
6. Decide whether Jira ticket IDs should prefix commit messages and pull request titles in this repo.
7. In Copilot Chat, ask: `Use product-owner to summarize the current instructions and available skills, ask whether Jira ticket IDs should prefix commit messages and PR titles, then tell me the next owner and the first durable artifact to create.`

## Workspace baseline

[`settings.json`](/home/sturlalange/Dev/my-claude-skills/.vscode/settings.json) makes the repo guidance more visible to Copilot features in VS Code:

- code generation keeps VS Code's file-based instruction path enabled instead of using deprecated settings-based code-generation instructions
- `.github/instructions/` and `.claude/rules/` are enabled as instruction-file locations
- referenced instruction files are allowed into chat context
- `.github/agents/` stays enabled as the custom-agent location
- organization-level instructions and organization-level custom agents stay discoverable when the adopter's account has access
- selection review reads `.github/copilot-instructions.md` and `AGENTS.md`
- commit message generation gets repo instructions plus a Conventional Commit reminder
- pull request description generation gets repo instructions plus a verification and risk reminder
- `chat.agent.maxRequests = 6` leaves some headroom for agentic work without pushing toward unbounded request trees

## Recommended operating shape

- Keep `AGENTS.md` short and durable.
- Keep broadly applicable Copilot guidance in `.github/copilot-instructions.md`.
- Use `.github/instructions/*.instructions.md` when folder-specific guidance would otherwise bloat repo-wide instructions.
- Treat `.vscode/settings.json` as a baseline, not as a guarantee that every adopter has identical local behavior.
- Document any required personal or org-level VS Code settings in onboarding docs instead of assuming the repo can force them.

## Verification

To verify the repo guidance is being picked up in VS Code:

1. Open Copilot Chat in this workspace.
2. Ask a question that should trigger the role model, for example: `Which role should own the next step for a non-trivial bug in this repo?`
3. Inspect the response references and confirm `AGENTS.md` or `.github/copilot-instructions.md` appear.
4. Try one custom agent from `.github/agents/` and confirm Copilot offers it in the agent picker.

## Limits

- This repo cannot reliably force Copilot sign-in, entitlement, model selection, or every runtime behavior from tracked files alone.
- Personal instructions and some IDE-level settings can override repo guidance.
- Copilot in VS Code has a weaker repo-native runtime control surface than `.claude/settings.json` or `.codex/config.toml`.
