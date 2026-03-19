---
name: refactor-safe
description: Perform behavior-preserving refactors with explicit invariants, staged edits, and regression gates. Use when the user asks to refactor, restructure, reorganize, or clean up code without changing external behavior.
argument-hint: "[file-or-module-scope]"
allowed-tools: Read, Grep, Edit, Bash(scripts/dev.sh:*), Bash(uv run pytest:*), Bash(uv run ruff:*)
---

# Safe Refactoring

## Goal

Improve structure and readability while preserving all externally observed behavior.

## Required Inputs

- Target scope (`$ARGUMENTS`)
- Refactor intent (readability, duplication reduction, modularity, etc.)

If scope is too broad, narrow to one module or one behavior slice first.

## Workflow

### 0. Read the target scope

Before any edits or invariant declarations, read:
- Target source file(s) — understand public API, class structure, existing patterns
- Corresponding test file(s) in `tests/<module>/` — understand current coverage
- `docs/STATUS.md` — check for in-flight work on this module

### 1. Define invariants first

Before edits, state what must not change:
- public method signatures
- return shapes/data contracts
- key user-visible behavior
- persistence side effects (DB writes, settings changes)

### 2. Lock behavior with tests

- Identify existing tests covering the scope.
- If coverage is weak, add characterization tests first.
- Run baseline targeted tests.

### 3. Refactor in stages

- Stage A: move/rename/restructure only
- Stage B: remove duplication / improve cohesion
- Stage C: final polish

After each stage:
```bash
uv run ruff check <touched-files>
uv run pytest <targeted-tests> -q
```

### 4. Run broader gates

```bash
scripts/dev.sh test-fast
scripts/dev.sh test-headless
```

If requested and display-capable:
```bash
scripts/dev.sh test-all
```

### 5. Report

See Output Contract below for required deliverables.

## Output Contract

Report:
- invariants declared and preserved
- staged refactor changes
- verification results (targeted + broader gates)
- remaining risks

## Failure Classification

After each verification run, classify issues as:
- **Behavior regression**: tests fail after a refactor stage — revert the last
  stage and make smaller moves.
- **Lint regression**: ruff violations introduced — fix before moving to next stage.
- **Environment blocker**: display/device errors unrelated to the refactor —
  report separately; run `scripts/dev.sh test-headless` to isolate.
- **Scope creep detected**: refactor uncovered a bug or design flaw — stop,
  flag for a separate task, do not fix inline.

## Guardrails

- No mixed feature additions inside a refactor commit unless user asks.
- Preserve externally observed behavior unless a separate behavior-change task
  is explicitly approved.
- Prefer many small safe moves over one large rewrite.
