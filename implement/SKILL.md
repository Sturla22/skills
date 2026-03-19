---
name: implement
description: Find and implement NotImplementedError stubs in the codebase. Use when asked to implement a stub, fill in a skeleton, build out a TODO, make a module functional, or replace a placeholder with working code.
argument-hint: "[module-or-class]"
---

# Implement Stubs

## Goal

Replace selected stubs with working behavior plus tests and lint-clean code.

## Required Inputs

- Target stub scope (`$ARGUMENTS` or discovered list)
- Expected behavior (if not obvious from tests/docs)

If behavior intent is ambiguous, ask before implementing.

## Workflow

### 1. Find stubs

If arguments are provided, search in that module/file. Otherwise, search the whole codebase:
```
grep -rn "raise NotImplementedError" src/skor/
```

Present the list of stubs found, grouped by module.

### 2. Confirm scope

Ask the user which stub(s) to implement if multiple are found and no specific one was requested.

### 3. Implement

For each stub to implement:

1. **Read the full file** to understand the class context, imports, and existing patterns
2. **Read the architecture docs** if needed:
   - `docs/ARCHITECTURE.md` for system design
   - `docs/references/` for technical guides (detection, tracking, physics, etc.)
   - `docs/requirements/` for functional requirements
   - `docs/DRILLS.md` for drill specifications
3. **Read existing tests** in the corresponding `tests/<module>/` directory
4. **Write tests** in the corresponding test file if they don't exist
5. **Run tests** with `uv run pytest tests/<module>/ -v` to verify, failing is fine at this stage (TDD; red-green-refactor)
6. **Implement** the method following project conventions:
   - SI units (meters, m/s, degrees) — never feet
   - Type hints on all signatures
   - Docstrings on public methods
   - `from __future__ import annotations` at top of file
   - Dataclasses for structured return types
   - Use `logging.getLogger(__name__)` for debug output
7. **Re-run tests** with `uv run pytest tests/<module>/ -v` to verify
8. **Run lint** with `uv run ruff check src/skor/<module>/` to verify
9. **Refactor** if appropriate

### 4. Report

Summarize what was implemented, any design decisions made, and test results.

## Guardrails

- Do not implement stubs whose behavior intent is unclear — ask first.
- Never change a public method signature unless the stub docstring explicitly
  requires it.
- Do not implement stubs in modules unrelated to the user's request scope.
- If a stub depends on another unimplemented stub, flag the dependency chain
  rather than guessing behavior.

## Failure Classification

After running tests, classify failures as:
- **Logic regression**: assertion errors, wrong return values, type mismatches
  in project code — these must be fixed before reporting success.
- **Missing dependency**: stub depends on another unimplemented method — flag
  and ask user whether to implement the dependency or mock it.
- **Environment blocker**: display errors, missing system tools, camera/device
  access — report as blocked, not as implementation failure.

## Output Contract

Report:
- stub(s) implemented
- tests added/changed
- verification commands and pass/fail
- open questions or assumptions
