---
name: skill-improve
description: Audit and iteratively improve Claude Code skills against best practices. Use when the user says "improve this skill", "audit skills", "skill quality check", "make skills better", or wants to optimize skill activation and execution quality.
argument-hint: "[skill-name | all]"
allowed-tools: Read, Grep, Glob, Edit
---

# Skill Improver

Autonomous audit-fix-verify loop for Claude Code skills, inspired by
autoresearch: read a skill, score it against a checklist, apply the
highest-impact fix, re-score, and repeat until converged or budget exhausted.

## Goal

Measurably improve targeted skills through iterative, checklist-driven edits
with before/after scoring.

## Required Inputs

- Target skill name (`$ARGUMENTS`) or `all` for a full audit pass
- Iteration budget (default: 3 rounds per skill)

If no target is specified, audit all skills and rank by improvement potential,
then start with the lowest-scoring skill.

## Best-Practice Checklist

Score each skill 0 or 1 on each criterion. A perfect skill scores 12/12.

### Frontmatter (4 points)

| # | Check | What to look for |
|---|-------|-----------------|
| F1 | **Trigger-rich description** | ≥3 natural-language trigger phrases after "Use when" (synonyms, user phrasings) |
| F2 | **No stale/hardcoded data** | No absolute paths, user-specific dirs, hardcoded dates, or time-sensitive tables |
| F3 | **argument-hint present** | Has `argument-hint` if the skill accepts arguments |
| F4 | **allowed-tools scoped** | `allowed-tools` is present and minimal (no wildcard `Bash(*)`) |

### Body — Structure (4 points)

| # | Check | What to look for |
|---|-------|-----------------|
| S1 | **Auto-research step** | Workflow starts by reading relevant files/context before any edits or commands |
| S2 | **Output contract** | Has an explicit "Output Contract" or "Report" section defining deliverables |
| S3 | **Guardrails** | Has guardrails/constraints section preventing common mistakes |
| S4 | **Concise intro** | Body intro ≤2 lines; no duplication of description; no "Use this skill when" |

### Body — Quality (4 points)

| # | Check | What to look for |
|---|-------|-----------------|
| Q1 | **Concrete commands** | Workflow steps include actual runnable commands, not just prose |
| Q2 | **Failure classification** | Distinguishes failure types (regression vs environment, code vs config, etc.) |
| Q3 | **Single responsibility** | Skill does one job; doesn't try to be two skills in one |
| Q4 | **No redundant sections** | No duplicate info between sections; references aren't repeated as prose |

## Workflow

### 1. Score the target skill

Read the skill file and score each of the 12 checks:

- **Single skill** — use Read on `.claude/skills/<target>/SKILL.md`
- **Batch mode** — use Glob with `.claude/skills/*/SKILL.md` to list all skills,
  then Read each one

Present the scorecard:

```
<skill-name>: 9/12
  F1: ✓  F2: ✓  F3: ✓  F4: ✓
  S1: ✗  S2: ✓  S3: ✗  S4: ✓
  Q1: ✓  Q2: ✗  Q3: ✓  Q4: ✓
```

### 2. Identify the highest-impact fix

Pick the failing check that would most improve the skill's activation rate
or execution quality. Priority order: F1 > S1 > F2 > S2 > S3 > Q2 > rest.

State the fix plan in one sentence before editing.

### 3. Apply the fix

Edit the SKILL.md with the smallest change that addresses the failing check.
Follow the same conventions as existing skills (see sibling skill files for
patterns).

### 4. Re-score

Re-read the edited file and re-score. Present the updated scorecard with
the delta:

```
<skill-name>: 10/12 (+1)
  S1: ✗ → ✓
```

### 5. Iterate or stop

- If score improved and iteration budget remains, go to step 2.
- If score did not improve, revert the last edit and try a different fix.
- If all checks pass (12/12) or budget exhausted, stop.

### 6. Report

For each skill touched, present:
- before/after score
- changes made (one line each)
- remaining gaps (if any)

## Batch Mode (`all`)

When `$ARGUMENTS` is `all`:
1. Score every skill in `.claude/skills/*/SKILL.md`
2. Rank by score ascending (worst first)
3. Present the ranking table
4. Ask user: "Start improving from the bottom, or pick specific skills?"
5. Iterate on selected skills within budget

## Failure Classification

When a fix doesn't improve the score, classify why:
- **Misapplied fix**: edit didn't actually address the checklist criterion —
  revert and re-read the check definition.
- **Scope conflict**: fix for one check broke another check — revert and try
  a different approach.
- **Domain gap**: fix requires project-specific knowledge the auditor lacks —
  flag and skip.

## Guardrails

- Never delete a skill entirely — only edit SKILL.md content.
- Never change a skill's `name` field (breaks activation routing).
- Keep edits minimal and reversible — one check per iteration.
- If a fix requires domain knowledge you don't have (e.g. correct ML commands),
  flag it and skip rather than guessing.
- Do not add features or workflow steps that aren't backed by a checklist item.

## Output Contract

Report:
- skills audited
- before/after scorecards
- changes applied per skill
- remaining improvement opportunities
