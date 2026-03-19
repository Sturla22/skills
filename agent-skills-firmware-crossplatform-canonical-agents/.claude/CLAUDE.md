# Claude Code Project Instructions

See @../AGENTS.md for the role model and default workflow order.

## Project goals

This starter repo is optimized for embedded firmware teams that want:
- reusable skills instead of giant prompts
- clear separation between planning, implementation, verification, and review
- interfaces that survive platform migration
- host-side simulation and characterization where possible
- explicit safety and resource thinking

## Replace these placeholders for your real project

### Build commands
- Primary configure: `cmake -S . -B build`
- Primary build: `cmake --build build`
- Primary test: `ctest --test-dir build --output-on-failure`
- Lint / static analysis: `TODO`
- Host simulation tests: `TODO`
- Hardware integration tests: `TODO`

### Key directories
- Application code: `src/`
- HAL / platform: `platform/`
- Drivers: `drivers/`
- Tests: `tests/`
- Docs / ADRs: `docs/`

## Working rules

- Read the relevant skill before doing a complex task.
- Prefer the smallest useful diff.
- Before changing hardware-facing code, make the interface and test seam explicit.
- Before risky refactors, add characterization tests.
- Before claiming a bug is fixed, prove the original symptom was reproducible or at least well-characterized.
- Update docs when architecture, contracts, failure behavior, or migration paths change.

## Firmware-specific rules

- Keep units explicit in names, comments, or types.
- Keep ISR / thread / task context assumptions explicit.
- Avoid hidden global state.
- Avoid speculative abstraction and future-proofing with no near-term caller.
- Be conservative with dynamic allocation, blocking behavior, and retry loops.
- Prefer assertions for violated internal invariants and explicit error returns for expected external failures.
- Log at boundaries that matter, not everywhere.

## Deliverable expectations

Every substantial task should leave behind:
- a plan or rationale
- code or doc changes
- evidence of verification
- a short statement of residual risk
