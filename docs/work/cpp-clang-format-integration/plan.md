# Work Plan

## Storage

- Work ID: `cpp-clang-format-integration`
- File path: `docs/work/cpp-clang-format-integration/plan.md`
- Source brief: `docs/work/cpp-clang-format-integration/brief.md`

## Problem statement
Add a canonical `clang-format` style and integrate it into the repo’s local and CI C++ workflow alongside the existing `clang-tidy` baseline.

## Scope
- Add `.clang-format` for the starter
- Add repo-owned format and format-check entrypoints
- Wire `clang-format` into `pre-commit`, bootstrap, and `ci-checks`
- Update docs

## Non-goals
- Formatting non-C/C++ files
- Replacing the current static-analysis stack
- Broad style churn outside the starter

## Key behavior rules / scenarios
- Local formatting should be auto-fixing through `pre-commit`
- CI should check formatting without mutating files
- The chosen style should preserve the starter’s current brace and indentation conventions

## Preferred test strategy
- Run the formatter over the starter
- Validate the formatter check
- Run `pre-commit` on the `clang-format` hook
- Rerun `make ci-checks`
- Validate the work packet

## Exit criteria / milestone criteria
- `make format-cpp` works
- `make check-clang-format` passes
- `python3 -m pre_commit run --all-files clang-format` passes
- `make ci-checks` passes
- `python3 tools/cli.py check-work cpp-clang-format-integration` passes

## Plan steps
1. Define the starter `.clang-format` style.
2. Add repo-owned format and check entrypoints in Python.
3. Wire the formatter into `pre-commit`, bootstrap, and `ci-checks`.
4. Update docs and work-packet evidence.
5. Run verification commands and record the result.
