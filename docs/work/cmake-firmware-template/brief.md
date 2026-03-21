# Product Brief

## Storage

- Work ID: `cmake-firmware-template`
- File path: `docs/work/cmake-firmware-template/brief.md`

## Request summary
Add a reusable CMake-based embedded firmware starter to this repo, with configure-time architecture enforcement, a `gcc-arm-none-eabi` toolchain-file example, and a minimal hello-world application for Nordic's nRF52840.

## Problem / desired outcome
This repo already recommends embedded-friendly workflow habits, but it does not yet ship a concrete firmware starter that demonstrates those habits in code. The desired outcome is a copyable starter under `extras/` that shows a sane CMake layout, architecture guardrails, host-side verification, and a target-side cross-build path.

## Why this matters
Without a concrete starter, adopters still have to invent the build shape, architecture checks, and target wiring themselves. That weakens the repo's value as a practical embedded starting point.

## Code drivers
Selected drivers for this work:

- User scenarios — give adopters a concrete firmware starter they can copy.
- Design intent communication — encode how the repo expects CMake, layering, and Pitchfork layout to fit together.
- Epistemic uncertainty — reduce ambiguity about what "use CMake here" means in practice.

Which of the following justify this work?

- User scenarios — enables or improves a real actor workflow
- Risk — addresses a known failure mode, safety, security, or reliability concern
- Epistemic uncertainty — a spike or prototype to reduce unknowns before committing to a design
- Design intent communication — types, assertions, structure, or naming chosen to make intent explicit for future maintainers
- External obligation — regulatory, certification, or standards mandate

Code traceable to none of these is a candidate for removal, not refinement.

## Stakeholders / users
- Teams adopting this starter repo for embedded firmware work
- Maintainers of this repo's public contract
- AI-assisted developers who need a machine-readable and reproducible build baseline

## Stakeholder needs / system outcomes
- A concrete CMake starter that matches the repo's existing guidance
- A target-ready `gcc-arm-none-eabi` toolchain example
- Mechanical enforcement of basic architecture boundaries
- A verification path that does not depend only on hardware access

## Design criteria / key parameters
- Keep the starter inside Pitchfork-recognized layout under `extras/`
- Use CMake Presets for checked-in host and target configurations
- Enforce architecture constraints at CMake configure time
- Provide a host-side verification path plus a real cross-build path
- Keep the template dependency-free: no vendored Nordic SDK required for the starter itself

## In scope
- New starter project under `extras/cmake-nrf52840-template/`
- Toolchain file for `gcc-arm-none-eabi`
- Configure-time architecture enforcement module
- Hello-world firmware target for nRF52840
- Host-side tests, including a negative test that proves architecture enforcement
- Repo docs and changelog updates that point to the new starter
- Work packet and verification evidence for this change

## Out of scope
- Zephyr, west, or vendor-SDK integration
- Flashing scripts, debug-probe automation, or HIL workflows
- Production-grade Nordic BSP or HAL coverage beyond the minimal starter
- Broad refactors to repo-wide workflow docs outside the CMake starter path

## Constraints
- Preserve the repo's documented contract and update it deliberately
- Keep new files in Pitchfork-approved locations
- Avoid adding external dependencies for the starter's host tests
- Target the Nordic `nRF52840`

## Commit and PR title policy

- Should Jira ticket IDs prefix commit messages? Not required for this repo task.
- Should Jira ticket IDs prefix PR titles? Not required for this repo task.

## Existing conventions to preserve

- Existing issue tracker, commit, or PR conventions: Prefer Conventional Commits.
- Existing release or branching process: Keep changes additive and SemVer-aware.
- Existing docs, ADR, or architecture layout: Use `docs/work/cmake-firmware-template/` and Pitchfork-recognized top-level directories.
- Existing build, test, and CI expectations: Use repo-local checks where possible, and verify template behavior with real CMake commands.
- Existing agent, instruction, or automation files: Preserve `.agents/` as canonical and update docs contract surfaces explicitly.

## System context / external interfaces
- CMake and CTest
- GNU Arm Embedded Toolchain (`arm-none-eabi-gcc` and friends)
- Nordic nRF52840 memory map assumptions for a bare-metal example
- Repo docs, changelog, and Pitchfork layout checks

## Acceptance criteria
- `extras/cmake-nrf52840-template/` exists and is documented
- The starter provides checked-in host and cross-build presets
- The starter fails CMake configure on an invalid internal dependency edge
- The host preset builds and passes its tests
- The cross-build preset produces an ELF for the nRF52840 starter
- Repo docs point to the starter and explain the CMake default clearly
- `CHANGELOG.md` records the addition under `Unreleased`

## Measures of effectiveness / performance
- A new adopter can build host checks and the cross target using copyable commands from the starter README
- Architecture enforcement is proven by an automated negative test, not only by prose
- The starter remains small enough to understand in one sitting

## Behavior rules / examples (BDD)
- Given a domain library, when it links against a platform library directly, configure should fail.
- Given a host developer without hardware attached, when they build the host preset, tests should run and prove the hello service behavior plus architecture enforcement.
- Given a developer with `gcc-arm-none-eabi` installed, when they build the target preset, the starter should emit a firmware ELF and binary artifacts for nRF52840.

## Behavior scenarios (BDD)
- Scenario: An adopter wants a concrete CMake starter instead of only repo guidance.
  Outcome: The repo provides a copyable starter under `extras/`.
- Scenario: An adopter accidentally links the domain layer to the platform layer.
  Outcome: CMake configure fails before the build proceeds.
- Scenario: An adopter wants to verify the template on a laptop before touching hardware.
  Outcome: Host tests run through CTest.
- Scenario: An adopter wants to generate firmware artifacts for an Arm Cortex-M target.
  Outcome: The toolchain preset produces the target ELF and post-build artifacts.

## Derived requirements / traceability notes
- Because this is a public starter addition, update `README.md`, `docs/firmware-playbook.md`, and `CHANGELOG.md`
- Because the repo documents Pitchfork compliance, the starter must live under `extras/`
- Because this is non-productized tooling/docs work, TDD may be waived if explicit verification replaces it

## Public contract / compatibility impact
Backward-compatible addition to the documented starter-repo contract. No existing path is removed or renamed.

## Delivery class
Non-productized tooling / starter-template work.

## TDD expectation
TDD is intentionally waived. The replacement verification is: host configure/build/test, a negative architecture-enforcement test, target cross configure/build, and repo layout/work-packet checks.

## Validation intent / evidence
Validation is limited to proving the starter is understandable and runnable as documented. No separate user study is planned in this slice.

## SemVer / changelog expectation
`MINOR`-class addition to the repo contract. Update `CHANGELOG.md` under `Unreleased`.

## Assumptions
- The starter targets `nRF52840`
- The local environment has CMake and the Arm GNU toolchain available for verification
- Semihosting is an acceptable minimal "hello world" transport for the bare-metal target example

## Open questions
- Whether a later follow-up should add flashing/debug presets or keep this starter build-only
- Whether a later follow-up should add a Zephyr-based alternative starter

## Recommended next owner(s)
- `developer` for implementation
- `verifier` after the starter and docs are in place

## Parallelization notes
No parallel write lanes. The starter files, docs, and work packet share too much context for clean isolation.

## Delegation notes
Implementation stays in the main thread for this slice.
