# Product Brief

## Storage

- Work ID: `cpp-static-analysis-stack`
- File path: `docs/work/cpp-static-analysis-stack/brief.md`

## Request summary
Turn the C++ static-analysis research into a concrete recommendation for this repo, including what to run in-editor, pre-commit, and CI, and make `pre-commit` mean the actual Python package rather than a generic checkpoint.

## Problem / desired outcome
Choose a practical static-analysis baseline that fits this repo’s current C++ surface and existing workflow rules, then make that baseline concrete enough to run and document.

## Why this matters
The research file explains the tool landscape, but the repo still needs an actual local and CI operating model. Without a concrete baseline, “use static analysis” stays abstract and easy to ignore.

## Code drivers
Selected drivers for this work:

- User scenarios — developers need one clear command for local gating and CI.
- Risk — architecture and firmware starter code should have an analyzer baseline that catches real mistakes early.
- Design intent communication — the repo should show a concrete, low-complexity static-analysis posture instead of a placeholder.

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
- One primary static-analysis command that is simple enough to keep in normal use
- Editor guidance that matches the starter’s host-vs-target split
- Real `pre-commit` framework support when the docs say “pre-commit”
- CI integration that stays thin and delegates to repo-owned scripts
- An explicit record of what is intentionally not being added yet

## Design criteria / key parameters
- Prefer one primary enforced analyzer over a broad tool pile
- Reuse existing CMake presets and `compile_commands.json`
- Keep workflow YAML thin and put substantive logic in repo-owned scripts
- Avoid adding a hosted analysis platform or enterprise service for this repo’s current size

## In scope
- Repo-specific recommendation for editor, pre-commit, and CI use
- Repo-owned command surface for the recommended baseline
- Minimal `pre-commit` framework wiring around the existing analyzer command
- Documentation updates and a durable recommendation record

## Out of scope
- Integrating CodeQL, SonarQube, or PVS-Studio into this repo today
- Establishing a second mandatory analyzer gate
- Benchmarking analyzer performance or false-positive rates

## Constraints
- Follow the repo rule preferring thin CI YAML and repo-tracked scripts
- Keep the C++ analyzer recommendation grounded in the actual starter already in the repo
- Use `tools/cli.py check-work` to validate the packet

## Commit and PR title policy

- Should Jira ticket IDs prefix commit messages? Not applicable to this slice.
- Should Jira ticket IDs prefix PR titles? Not applicable to this slice.

## Existing conventions to preserve

- Existing issue tracker, commit, or PR conventions: Keep Conventional Commit compatibility.
- Existing release or branching process: No release is in scope for this turn.
- Existing docs, ADR, or architecture layout: Use the standard work-packet structure and current-state docs tone.
- Existing build, test, and CI expectations: Keep CI logic in `tools/` and `Makefile` rather than in workflow YAML.
- Existing agent, instruction, or automation files: Update the canonical `.agents/project/CLAUDE.md` surface and resync generated output.

## System context / external interfaces
- Existing CMake starter under `extras/cmake-nrf52840-template/`
- Existing GitHub Actions workflow already calling `make ci-checks`
- Existing research packet `docs/work/cpp-static-analysis-research/`

## Acceptance criteria
- A durable recommendation exists under `docs/work/cpp-static-analysis-stack/evidence/`
- The repo has a concrete primary static-analysis command
- The repo has a real `.pre-commit-config.yaml` that invokes the analyzer gate
- Documentation states what to use in-editor, pre-commit, and CI
- CI can pick up the analyzer baseline through existing repo-owned entrypoints

## Measures of effectiveness / performance
- The final answer can name one recommended enforced analyzer and one concrete command
- The recommendation is consistent with the repo’s thin-CI rule
- The starter README gives actionable guidance without requiring chat context

## Behavior rules / examples (BDD)
- Given a developer editing domain or host-test code, the docs should point them at the host compile database.
- Given a developer editing firmware or platform code, the docs should point them at the target compile database.
- Given CI, the analyzer gate should be reachable through `make ci-checks`, not bespoke workflow shell fragments.

## Derived requirements / traceability notes
- The recommendation should reuse the earlier research rather than restating the whole market landscape
- The baseline should stay intentionally smaller than an enterprise C++ analyzer stack

## Public contract / compatibility impact
This changes the documented repo contract by replacing the static-analysis placeholder with a concrete command and documented starter guidance.

## Delivery class
Non-productized tooling and documentation work.

## TDD expectation
TDD skipped. This slice is repo tooling and docs integration; verification is command execution and packet validation rather than behavior-first product development.

## Validation intent / evidence
Validation is limited to whether the chosen command runs successfully on the starter and whether the documented recommendation is clear enough to follow.

## SemVer / changelog expectation
Changelog entry expected under `Unreleased` because the repo’s documented workflow changes.

## Assumptions
- For this repo’s current size, `clang-tidy` is the right primary enforced analyzer
- `cppcheck` and platform services can be deferred without weakening the baseline too far

## Open questions
- Whether `cppcheck` should later be added as a second non-blocking or scheduled pass
- Whether future repo growth will justify CodeQL or another platform-layer analyzer

## Recommended next owner(s)
- `developer` to wire the command surface and docs
- `verifier` to confirm the command runs and the packet validates

## Parallelization notes
No parallel write lanes used.

## Delegation notes
Work performed directly in the control thread using the earlier research packet as input.
