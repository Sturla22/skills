# Work Plan

## Storage

- Work ID: `cmake-firmware-template`
- File path: `docs/work/cmake-firmware-template/plan.md`
- Source brief: `docs/work/cmake-firmware-template/brief.md`

## Problem statement
Add a concrete embedded CMake starter to this repo so the repo's CMake guidance is backed by a runnable example with architecture enforcement, host verification, and Arm cross-build support.

## Stakeholders / system context
- Primary consumers are adopters of this starter repo
- The change touches the repo's documented public contract
- The starter will live under `extras/`, not as the root build for this repo

## Scope
- Add the starter project under `extras/cmake-nrf52840-template/`
- Add docs that make CMake the repo's default embedded build recommendation
- Update the changelog
- Record verification evidence in the work packet

## Non-goals
- Replace this repo's own Python/CLI workflow with a root CMake build
- Add vendor SDKs or flashing automation
- Build a full Nordic BSP

## Requirements / constraints / assumptions to keep visible
- Keep the starter in a Pitchfork-approved location
- Target the Nordic `nRF52840`
- Keep architecture enforcement mechanical, not just documented
- Use explicit verification because TDD is waived for this non-productized tooling slice

## Public contract / compatibility impact
Adds a new optional starter path and new documented default guidance. Existing paths remain intact.

## SemVer / changelog expectation
`MINOR`-class additive change; update `CHANGELOG.md`.

## Key behavior rules / scenarios
- Invalid `domain -> platform` dependency edges must fail at configure time
- Host preset must run fast local checks without hardware
- Target preset must cross-build firmware artifacts for the nRF52840 starter

## Trade studies / decision points
- Use `extras/` rather than making the repo root a firmware project
- Use semihosting rather than a vendor SDK UART path for the minimal target hello world
- Use CMake configure-time graph checks rather than a separate custom script for architecture enforcement

## Preferred test strategy
- Lowest-level check: host executable test for the hello service behavior
- Architecture check: negative CTest case that expects configure failure on an invalid dependency edge
- Cross-build check: configure and build the nRF52840 preset with `arm-none-eabi-g++`
- Repo checks: `tools/cli.py check-layout` and `tools/cli.py check-work cmake-firmware-template`

## Validation plan
- Confirm the starter README is enough to reproduce the verified commands
- Defer broader adopter validation to future repo usage; this slice proves technical viability, not long-term fit

## Walking skeleton
1. Minimal layer stack (`contracts`, `domain`, `platform`, `app`)
2. Host test for `HelloService`
3. Configure-time architecture enforcement
4. Cross-build target with startup file, linker script, and post-build artifacts
5. Docs and changelog wired to the starter

## Minimal configuration / iteration target
One starter project in `extras/` with one host test executable and one nRF52840 firmware executable.

## Exit criteria / milestone criteria
- The starter configures and builds on host for tests
- The negative architecture test passes by failing as expected
- The target preset builds successfully with the Arm toolchain
- Repo docs and changelog reflect the new starter
- Work packet is complete and verification evidence is recorded

## Plan steps
1. Create the starter layout under `extras/cmake-nrf52840-template/` with CMake presets, toolchain file, architecture module, source, and tests.
2. Implement the hello-world domain/platform/app split and the bare-metal nRF52840 startup/linker wiring.
3. Add a negative configure test that proves the architecture rule is enforced.
4. Update `README.md`, `docs/firmware-playbook.md`, and `CHANGELOG.md`.
5. Run host checks, cross-build checks, and repo packet/layout checks; record the evidence.

## Parallel lanes

For each active lane, capture:
- lane name
- owner
- write surface
- worktree / isolation plan
- merge point / integration checkpoint

No active parallel lanes.

## Ownership boundaries
- This plan covers implementation plus verification of the new starter
- It does not include a separate release-management or technical-writer lane

## Blockers / dependencies
- Local availability of CMake, Ninja, and `arm-none-eabi` binaries
- Linker/startup correctness for the minimal semihosting example

## Verification gates
- Host preset configure/build/test succeeds
- Negative architecture test is exercised and passes
- Cross-build preset configure/build succeeds
- Repo packet and layout checks succeed
- Verification evidence file is written

## Risks / unknowns
- The target request may have intended a different Nordic MCU
- Semihosting support may vary across debug environments even if the binary links cleanly
- Configure-time dependency inspection must handle only internal targets and avoid false positives

## Escalation triggers
- If the Arm toolchain cannot link the minimal semihosting binary without extra runtime work beyond the current slice
- If a different Nordic MCU is required than `nRF52840`
