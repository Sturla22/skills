# Work Packets

Store durable task context under this folder.

## Goal

Keep one canonical home for shared context so briefs, plans, status, evidence, and handoffs work together instead of repeating each other.
Use `docs/workflow-experiments/` separately for bounded process-improvement experiments; keep this folder focused on product or task work packets.

## Work packet structure

Create one folder per work item under `docs/work/<work-id>/`.

Recommended layout:

```text
docs/work/<work-id>/
├── brief.md
├── plan.md
├── status.md
├── evidence/
│   ├── bounded-autonomy-loop.md
│   ├── verification.md
│   ├── hypotheses/
│   │   └── HYP-001-short-title.md
│   └── optimization-scorecard.md
└── handoffs/
    └── 001-product-owner-to-planner.md
```

## Ownership model

- `brief.md` is the canonical shared-understanding record. `product-owner` owns it.
- `plan.md` is the canonical execution plan. `planner` owns it.
- `status.md` is the current owner / blocker / next-action snapshot. `product-owner` owns the overall truth; the current owner updates it when the state changes.
- `evidence/` is for durable proof and investigation artifacts.
- `handoffs/` is for role-to-role delta records.
- When parallel lanes are active, `plan.md` and `status.md` should also name the worktree or other isolation used for each active write lane.

## Handoff convention

- Store one Markdown file per handoff under `docs/work/<work-id>/handoffs/`.
- Name files with a sortable prefix and role transition, for example:
  - `001-product-owner-to-planner.md`
  - `002-planner-to-developer.md`
  - `003-developer-to-verifier.md`
- If a task branches into parallel lanes, include the lane in the file name:
  - `004a-planner-to-developer-lane-a.md`
  - `004b-planner-to-reviewer-lane-b.md`
- Handoffs should point to `brief.md`, `plan.md`, `status.md`, and relevant evidence files, then record only what changed.

## Work ID guidance

- Prefer an existing bug ID, task ID, or issue key.
- If none exists, use a short kebab-case slug that is stable for the life of the work item.

## Templates

- `templates/product-brief-template.md` -> `docs/work/<work-id>/brief.md`
- `templates/work-plan-template.md` -> `docs/work/<work-id>/plan.md`
- `templates/work-status-template.md` -> `docs/work/<work-id>/status.md`
- `templates/bounded-autonomy-loop-template.md` -> `docs/work/<work-id>/evidence/bounded-autonomy-loop.md`
- `templates/handoff-template.md` -> `docs/work/<work-id>/handoffs/<sequence>-<from>-to-<to>.md`
- `templates/verification-template.md` -> `docs/work/<work-id>/evidence/verification.md`
- `templates/hypothesis-template.md` -> `docs/work/<work-id>/evidence/hypotheses/HYP-001-short-title.md`
- `templates/optimization-scorecard-template.md` -> `docs/work/<work-id>/evidence/optimization-scorecard.md`
- `templates/workflow-experiment-template.md` -> `docs/workflow-experiments/<experiment-id>.md`

## Non-intrusive structure

- Keep durable task context under `docs/work/`.
- Do not mix work packets into top-level architecture docs, playbooks, or ADRs.
- Link from release notes, ADRs, or architecture docs when useful, but keep the task context here.
