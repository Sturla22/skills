# Product Brief

## Storage

- Work ID: `cpp-clang-format-integration`
- File path: `docs/work/cpp-clang-format-integration/brief.md`

## Request summary
Add `clang-format` to the repo’s existing C++ quality tooling.

## Problem / desired outcome
Extend the starter’s C++ tooling so formatting is defined, easy to run locally, enforced in CI, and integrated into the actual `pre-commit` framework path already used for `clang-tidy`.

## Why this matters
The repo now has a concrete `clang-tidy` baseline and real `pre-commit` support, but it still lacks a canonical formatter. That leaves C/C++ style decisions implicit and makes hook-driven cleanup incomplete.

## Code drivers
Selected drivers for this work:

- User scenarios — developers need one clear formatting command and an automatic local hook.
- Design intent communication — the starter should show an explicit C/C++ formatting policy, not just a static-analysis policy.
- Risk — automatic formatting reduces noisy review churn and keeps style drift out of CI.

Which of the following justify this work?

- User scenarios — enables or improves a real actor workflow
- Risk — addresses a known failure mode, safety, security, or reliability concern
- Epistemic uncertainty — a spike or prototype to reduce unknowns before committing to a design
- Design intent communication — types, assertions, structure, or naming chosen to make intent explicit for future maintainers
- External obligation — regulatory, certification, or standards mandate

Code traceable to none of these is a candidate for removal, not refinement.

## Stakeholders / users
- Maintainers of this starter repo
- Developers using the embedded CMake starter
- Future adopters copying the starter into real firmware repositories

## Stakeholder needs / system outcomes
- A canonical `clang-format` style for the starter
- A direct formatter command and a non-mutating formatter check
- A `pre-commit` hook that actually formats changed starter C/C++ files
- CI enforcement that stays thin and repo-owned

## Design criteria / key parameters
- Keep the formatter aligned with the starter’s current Allman-style layout
- Reuse the same repo-owned automation model already used for `clang-tidy`
- Use Python for non-trivial automation
- Keep CI non-mutating while allowing the local hook to auto-format files

## In scope
- Starter `.clang-format` policy
- Repo-owned format and format-check entrypoints
- `pre-commit` hook integration for `clang-format`
- Documentation and a durable work packet

## Out of scope
- Formatting non-C/C++ file types
- Repo-wide formatting policy for Python, Markdown, or YAML
- Changing the starter to a materially different C++ style

## Constraints
- Keep CI YAML thin
- Keep the formatter scoped to starter C/C++ files
- Verify the hook path, direct command path, and aggregate CI path

## Acceptance criteria
- The starter has a checked-in `.clang-format`
- The repo has a direct format command and a direct format-check command
- `pre-commit` runs `clang-format` on changed starter C/C++ files
- `make ci-checks` enforces formatting without mutating files

## Delivery class
Non-productized tooling and documentation work.

## TDD expectation
TDD skipped. Verification is command execution and hook/CI validation.

## SemVer / changelog expectation
Changelog entry expected under `Unreleased`.
