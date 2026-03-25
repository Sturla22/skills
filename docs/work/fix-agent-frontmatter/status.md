# Work Status

## Storage

- Work ID: `fix-agent-frontmatter`
- File path: `docs/work/fix-agent-frontmatter/status.md`
- Brief: `docs/work/fix-agent-frontmatter/brief.md`
- Plan: `docs/work/fix-agent-frontmatter/plan.md`

## Current owner

- Role: developer
- Date: 2026-03-25
- Lane: main
- Worktree / isolation: primary working tree

## Current summary

Fixed both the Claude and GitHub agent generators so generated custom agent frontmatter emits YAML-safe quoted descriptions, then resynced the generated agent files.

## Current step

Hand off the verified fix.

## Last completed checkpoint

Updated `tools/cli.py`, regenerated `.claude/agents/*.md` and `.github/agents/*.agent.md`, passed `python tools/cli.py sync --check`, and confirmed YAML parsing for all generated agent files in both layouts.

## Open blockers

- None

## Active risks / unknowns

- No additional loader issues were found during repo-native sync validation.

## Continuous V&V status

- Verification: `python tools/cli.py sync --check` passed and all generated Claude and GitHub agent frontmatter blocks parsed successfully with PyYAML
- Validation: not applicable
- Integration: not applicable
- Open gaps: none identified for this slice

## Next action

Share the fix and validation results with the requester.

## Active evidence

- Verification:
  - `python tools/cli.py sync`
  - `python tools/cli.py sync --check`
  - PyYAML parse of every generated `.github/agents/*.agent.md` frontmatter block
  - PyYAML parse of every generated `.claude/agents/*.md` frontmatter block
- Hypotheses:
  - Confirmed: unquoted `description` plain scalars containing `:` caused the YAML parse failures.
- Optimization scorecard:
- Recent handoff:
