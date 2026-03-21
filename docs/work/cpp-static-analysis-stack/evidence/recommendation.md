# Recommendation: C++ Static-Analysis Baseline For This Repo

## Decision

Use `clang-tidy` as the repo’s first enforced C++ static-analysis baseline.

## Recommended operating model

### In-editor

- Use `clangd` or IDE-integrated `clang-tidy`.
- For `libs/domain/` and `tests/host/`, use `build/host-debug/compile_commands.json`.
- For `libs/platform/`, `src/main.cpp`, and `src/startup_nrf52840.c`, use `build/nrf52840-debug/compile_commands.json`.

### Pre-commit

- Install the framework with `make install-pre-commit`.
- Let the local `static-analysis` hook run `make check-static-analysis`.
- Use `python3 -m pre_commit run --all-files static-analysis` when you want to run the same hook manually.

### CI

- Keep CI thin and continue routing through repo-owned entrypoints.
- Include `make check-static-analysis` inside `make ci-checks`.

## Why this stack

- `clang-tidy` is the best fit for the repo’s current size and the existing CMake starter.
- The starter already exports `compile_commands.json`, so the main integration substrate is already present.
- `clang-tidy` gives one practical enforced gate for local use and CI without adding a hosted service or second mandatory analyzer.
- The repo already favors script-owned CI behavior, and the substantive analyzer entrypoint now lives in Python under `tools/ci/`, which matches the repo preference for non-trivial automation.
- The actual `pre-commit` package is now used for the local hook path, so the docs no longer overload “pre-commit” as a generic checkpoint term.

## Deliberate deferrals

- Do not add `cppcheck` as a mandatory gate yet. It remains a plausible future secondary pass, but it is not needed to establish a credible baseline and would add noise and policy complexity now.
- Do not add CodeQL, SonarQube, or PVS-Studio to this repo today. Those belong later if the repo grows into a materially larger or more security-driven C++ codebase.

## Tradeoffs accepted

- Editor support is split across host and target compile databases because the starter itself is split across host-tested and target-only surfaces.
- The repo script adds Arm GNU C++ include paths explicitly for target-side `clang-tidy` runs so that target C++ files analyze cleanly.
- Using one enforced analyzer is intentionally narrower than a full enterprise stack, but it is much more likely to stay enabled and understood.
