# CLI surface baseline

## Existing supported CLI operations reviewed

From `tools/cli.py`:

- `new-work` scaffolds `docs/work/<work-id>/` with `brief.md`, `plan.md`, `status.md`, `handoffs/`, and `evidence/`
- `new-handoff` creates the next numbered handoff file inside a work packet
- `new-scenarios` scaffolds `scenarios.md` either at project scope or inside a work packet
- `check-work` validates that required `brief.md` and `status.md` sections are filled
- `list-work` reports each work packet's current owner and step

## Workflow surfaces reviewed

- `AGENTS.md`
- `docs/operating-model.md`
- `.github/copilot-instructions.md`
- `README.md`
- `docs/workflow-experiments/EXP-004-force-work-packets-over-session-state.md`

## Conclusion

The main gap is guidance, not capability. The repo already has the supported CLI needed for work-packet scaffolding and inspection, so the smallest useful change is to state more explicitly that agents should use that CLI before hand-creating packet artifacts.
