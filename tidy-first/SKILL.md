---
name: tidy-first
description: Quick hygiene pass (naming, dead code, small duplication, lint fixes) without changing behavior. Use when the user says "clean up this code", "tidy before feature work", "quick cleanup", or the target area is messy and needs low-risk prep first.
argument-hint: "[file-or-module-scope]"
---

# Tidy First

Small, behavior-preserving cleanups before feature work.

## Goal

Reduce risk for the next change with low-risk tidy moves.

## Required Inputs

- Scope (`$ARGUMENTS`)
- Intended follow-up feature/change (if known)

If scope is broad, reduce to one file/module before editing.

## Workflow

### 0. Read before touching

Before any edits, read:
- Target file and its public API surface
- Corresponding test file in `tests/<module>/`
- `docs/STATUS.md` to check for active feature/refactor work on this module

### 1. Scope tightly

- Use the requested file/module only.
- Do not expand to unrelated cleanup.

### 2. Apply low-risk tidy moves

Allowed:
- rename unclear locals/params
- extract tiny helper functions
- remove dead code/imports/comments
- simplify duplicated conditionals
- align formatting with existing style

Avoid:
- architecture redesign
- API changes
- semantic behavior changes

### 3. Verify no behavior drift

Run:
```bash
uv run ruff check <touched-files>
uv run pytest <closest-tests> -q
```

### 4. Handoff

Report:
- what was tidied
- why it lowers risk
- evidence behavior stayed unchanged

## Failure Classification

After verification, classify issues as:
- **Behavior drift**: tests fail after tidy — revert the offending edit and
  try a smaller change.
- **Lint regression**: ruff violations introduced — fix before reporting.
- **Scope creep**: tidy uncovered a deeper issue — flag for a separate
  feature/refactor task, do not fix inline.

## Guardrails

- Keep diffs small and mechanical.
- If a cleanup requires behavior change, stop and switch to feature/refactor
  workflow.

## Output Contract

Report:
- tidy changes made
- why each change is low risk
- lint/test evidence for no behavior drift
