---
name: refactoring
description: Perform behavior-preserving refactors with explicit invariants, staged edits, and regression gates. Use when the user asks to refactor, restructure, reorganize, or clean up code without changing external behavior.
argument-hint: "[file-or-module-scope]"
allowed-tools: Read, Grep, Glob, Bash
---

# Refactoring

Improve structure and readability while preserving all externally observed behavior.

## Required Inputs

- Target scope (`$ARGUMENTS`)
- Refactor intent (readability, duplication reduction, modularity, etc.)

If scope is too broad, narrow to one module or one behavior slice first.

## Workflow

### 0. Read the target scope

Before any edits or invariant declarations, read:
- Target source file(s) — understand public API, class structure, existing patterns
- Corresponding test file(s) — understand current coverage (`Glob("**/{test,tests,spec}/**/*<module>*")`)
- Any status or in-flight docs (CLAUDE.md, STATUS.md, or equivalent) — check for active work on this module

### 1. Define invariants first

Before edits, state what must not change:
- public method signatures
- return shapes / data contracts
- key user-visible behavior
- persistence side effects (DB writes, settings changes)

### 2. Lock behavior with characterization tests

If coverage of the target area is weak, add characterization tests first (lock what the code *actually does*, not what it should do):
- Call the code, observe the output, record it as the expected value.
- These tests protect against unintended behavior change during the refactor.
- Run baseline targeted tests before the first edit.

### 3. Use the Mikado Method for large refactors

When a direct attempt reveals blocking dependencies:
1. Write down the refactor goal.
2. Attempt it. If it breaks: **revert all changes** — do not fix the breakage.
3. Write the blocking prerequisite as a child node.
4. Recurse: attempt each prerequisite; revert on failure; add its prerequisites.
5. Work from the leaves (no unresolved dependencies) upward.
6. Commit each passing leaf. The codebase stays green at every step.

### 4. Refactor in stages — two hats only

**Never wear two hats simultaneously.** At every moment you are either refactoring (structure, not behavior) or adding functionality (behavior, not structure). Switch hats between commits, not within one.

Atomic refactoring moves (pick one per step):
- **Extract Function / Inline Function** — the most-used moves; verify name adds clarity.
- **Rename** — use IDE-assisted rename to catch all references including dynamic dispatch.
- **Move Function / Move Field** — correct placement is the foundation of module design.
- **Replace Nested Conditional with Guard Clauses** — flatten early returns.
- **Sprout Technique** — extract new logic into a separately testable function; call it from legacy code without touching legacy internals.
- **Wrap Technique** — rename old method; create new method that delegates; add new behavior in wrapper.

After each atomic move, run lint and targeted tests:
```bash
# adapt to project toolchain (ruff/eslint/cargo clippy, pytest/jest/cargo test, etc.)
<lint-command> <touched-files>
<test-command> <targeted-tests>
```

### 5. Run broader gates

Run the project's broader regression suite:
```bash
<project-test-command>
```

### 6. Report

See Output Contract below for required deliverables.

## Output Contract

Report:
- invariants declared and preserved
- staged refactor changes (one line per atomic move)
- verification results (targeted + broader gates)
- remaining risks

## Failure Classification

After each verification run, classify issues as:
- **Behavior regression**: tests fail after a refactor stage — revert the last stage and make smaller moves.
- **Lint regression**: violations introduced — fix before moving to next stage.
- **Environment blocker**: display/device errors unrelated to the refactor — report separately; run a headless or reduced test suite to isolate.
- **Scope creep detected**: refactor uncovered a bug or design flaw — stop, flag for a separate task, do not fix inline.

## Guardrails

- No mixed feature additions inside a refactor commit unless user asks.
- Preserve externally observed behavior unless a separate behavior-change task is explicitly approved.
- Prefer many small safe moves over one large rewrite.
- When stuck: revert and map the prerequisite (Mikado) rather than pushing through a broken state.
- Scratch refactoring (explore by refactoring aggressively, then throw it away) is legitimate for comprehension — never commit it.
