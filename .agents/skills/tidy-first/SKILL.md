---
name: tidy-first
description: Quick hygiene pass (naming, dead code, small duplication, lint fixes) without changing behavior. Use when the user says "clean up this code", "tidy before feature work", "quick cleanup", or the target area is messy and needs low-risk prep first.
argument-hint: "[file-or-module-scope]"
allowed-tools: Read, Grep, Glob, Bash
---

# Tidy First

Small, behavior-preserving cleanups before feature work.

## Goal

Reduce risk for the next change with low-risk structural moves — leaving the code easier to understand and change without altering what it does.

## Required Inputs

- Scope (`$ARGUMENTS`)
- Intended follow-up feature/change (if known) — this determines which tidyings are worth doing

If scope is broad, reduce to one file/module before editing.

## Workflow

### 0. Read before touching

Before any edits, read:
- Target file and its public API surface
- Corresponding test file (`Glob("**/{test,tests,spec}/**/*<module>*")`)
- Any status or in-flight docs (CLAUDE.md, STATUS.md, or equivalent) — check for active work on this module

### 1. Scope tightly

- Use the requested file/module only.
- Do not expand to unrelated cleanup.
- Tidy only what makes the immediate follow-up change easier — not the whole file.

### 2. Apply named tidy moves (pick what is needed)

**Comprehension moves** (free, instant):
- **Chunk Statements** — insert blank lines between logically distinct sections in a function.
- **Explaining Variables** — extract a complex subexpression into a named variable.
- **Explaining Constants** — replace magic literals with named symbolic constants.
- **Explaining Comments** — add a comment only for the *why*, not the *what*.
- **Delete Redundant Comments** — remove comments that restate what the code says.
- **Reading Order** — rearrange code in the order a reader would prefer to encounter it.

**Structural moves** (minutes):
- **Guard Clauses** — replace deeply nested conditionals with early returns.
- **Dead Code** — delete unused code outright (version control is the safety net; do not comment out).
- **Remove Control Flag** — replace boolean loop-control variables with `break`/`return`/`continue`.
- **Cohesion Order** — move coupled elements adjacent; functions that change together go together.
- **Extract Helper** — pull a cohesive block into a named function when the name carries meaning.
- **New Interface, Old Implementation** — write the interface you wish existed; delegate to the old one; migrate call sites at your own pace.
- **One Pile** — inline everything back into one place before re-extracting, when prior abstractions obscure what the code does.

**Do not do:**
- Architecture redesign
- API changes or semantic behavior changes
- Tidying that takes longer than the feature it's preparing for

### 3. One kind of change at a time

Every commit is either structural (tidy) or behavioral. Never both. Reviewers can approve pure structural changes with minimal scrutiny; mixing them forces expensive review of the whole diff.

### 4. Verify no behavior drift

Run the project's lint and closest tests:
```bash
# adapt to project toolchain (ruff/eslint/cargo clippy, pytest/jest/cargo test, etc.)
<lint-command> <touched-files>
<test-command> <closest-tests>
```

### 5. Handoff

Report:
- what was tidied (one line per tidy move)
- why it lowers risk for the follow-up change
- evidence behavior stayed unchanged

## When to tidy (decision guide)
- **Tidy first** — the tidying directly makes the behavioral change cheaper or more understandable, and takes less time than the behavioral change it enables.
- **Tidy after** — behavioral change is urgent; tidy immediately after in a separate commit.
- **Tidy never** — code that genuinely will never be touched again (archived, retired).

## Failure Classification

After verification, classify issues as:
- **Behavior drift**: tests fail after tidy — revert the offending edit and try a smaller change.
- **Lint regression**: violations introduced — fix before reporting.
- **Scope creep**: tidy uncovered a deeper issue — flag for a separate feature/refactor task, do not fix inline.

## Guardrails

- Keep diffs small and mechanical.
- If a cleanup requires behavior change, stop and switch to feature/refactor workflow.
- If you have been tidying for more than one hour before the behavioral change, you have over-scoped; do only what's needed.

## Output Contract

Report:
- tidy changes made (one line per move, with the move name)
- why each change lowers risk for the follow-up
- lint/test evidence for no behavior drift
