# Firmware Playbook

Use this as the place to encode repo-specific engineering norms.

## Project Layout (Pitchfork)

This repo follows the [Pitchfork C++ project layout](https://vector-of-bool.github.io/2018/09/16/layout-survey.html).

| Directory | Purpose |
|---|---|
| `src/` | Source files; private headers; public headers if using merged placement |
| `include/` | Public headers only — use for separate header placement |
| `libs/` | Sub-libraries: HAL, BSP, drivers, OS abstraction, each with its own `src/` |
| `tests/` | All test source; mirrors the source layout where practical |
| `external/` | Vendored or submodule third-party dependencies — do not modify directly |
| `tools/` | Build scripts, code generators, CI helpers |
| `data/` | Static data: configs, calibration tables, test fixtures |
| `extras/` | Examples, benchmarks, integration demos — not required by the main build |
| `docs/` | Documentation, ADRs, work packets |
| `build/` | Build artifacts — not tracked in VCS |

### Header placement

Choose one and apply it consistently across the project:

- **Merged** (simpler; preferred for single-library firmware): public and private headers alongside source in `src/`
- **Separate** (preferred when the public API is a stable, versioned contract): public headers in `include/<project-name>/`, private headers in `src/`

### Embedded conventions

- HAL, BSP, and driver layers are sub-libraries under `libs/`: `libs/hal/`, `libs/bsp/`, `libs/drivers/<name>/`
- RTOS port or OS abstraction: `libs/os/` or `libs/rtos/`
- Linker scripts, startup files, vector tables: `src/` or `libs/startup/`
- Platform-specific code lives inside a sub-library, not as a sibling of `src/`

### Enforcement

`planner` names the target Pitchfork directory for every new file before implementation starts.
`developer` places files there and flags misplaced files as structural debt to fix in a separate tidy commit.
See `.claude/rules/pitchfork-layout.md` for the full rule set applied to source paths.

## Build System Default

This starter repo standardizes on **CMake** for concrete embedded build examples and starter layouts.

Why this is the default here:

- checked-in **CMake Presets** keep host and cross builds reproducible
- **toolchain files** make `gcc-arm-none-eabi` configuration explicit instead of shell-local
- **CTest** gives a simple host-side verification path before hardware work
- **dependency scanning** catches known vulnerabilities in `external/` vendored code before they ship
- the target graph is visible enough to enforce a small architecture policy at configure time

Use [`extras/cmake-nrf52840-template/`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template) as the concrete starting point when you want a copyable embedded CMake baseline.

## Strong defaults

- Name interfaces in terms of **capabilities**, not vendor details, when the abstraction is intended to survive platform migration.
- Keep **policy** separate from **mechanism**.
- Prefer **pure or mostly pure decision logic** above the HAL boundary.
- Keep **units, ownership, timing, and error semantics** obvious.
- Prefer **deterministic tests** over log-reading as the primary proof.
- When optimizing, count expensive indirect operations behind a seam or measure direct RAM/flash footprint explicitly, then compare before/after results instead of guessing.

## MISRA and restricted language subsets

When the product context demands a coding standard (safety-critical, regulated, or high-reliability):

- Choose a compliance level before writing code: **mandatory**, **required**, or **advisory** rules from MISRA C:2023 or MISRA C++:2023.
- Configure `clang-tidy` with MISRA-adjacent checks (e.g., `bugprone-*`, `cert-*`, `cppcoreguidelines-*`) as a practical starting point when full MISRA tooling is not yet available.
- Document deviations explicitly — each deviation needs a rationale and reviewer sign-off.
- Domain-specific standards (ISO 26262, IEC 62304, IEC 61508, DO-178C) may impose additional coding rules beyond MISRA — identify the applicable standard early.
- Treat static-analysis warnings in safety-critical paths as defects, not suggestions.

## Memory safety strategy

- For new modules where the toolchain supports it, consider Rust as the default to eliminate memory-safety defects at compile time.
- For existing C/C++ code, prefer safe patterns: bounded containers (ETL), RAII for resource ownership, span/view over raw pointer arithmetic, and explicit lifetime annotations in comments.
- Encapsulate unavoidable unsafe code (raw hardware access, inline assembly, vendor SDK calls) behind narrow verified interfaces.
- Run memory-error detectors (ASan, MSan, UBSan) in host-test builds to catch issues that static analysis misses.
- Treat memory-safety defects (buffer overflow, use-after-free, double-free, uninitialized read) as high-severity — they are the dominant class of exploitable vulnerabilities in systems code.

## Things to record for each subsystem

- responsibilities
- state ownership
- concurrency model
- timing constraints
- resource budgets
- external dependencies
- reboot / timeout / partial-write behavior
- how it can be simulated on host
- how it is verified on target hardware
- power-state behavior: sleep/wake transitions, brownout detection, peripheral power gating
- battery and charging edge cases if applicable

## Feature flags and compile-time toggles

- Use compile-time feature flags (`#if FEATURE_X_ENABLED`) to isolate incomplete or experimental functionality during development.
- Keep the default build clean: all shipping features enabled, all experimental features disabled unless explicitly opted in.
- Document each flag's purpose, expected lifetime, and removal criteria.
- Do not ship debug-only or test-only flags in production builds — gate them behind a build type or preprocessor guard.
- For runtime configuration (e.g., enabling a feature via NVM settings or cloud config), define the default behavior and the fallback if the configuration is missing or corrupt.
- Remove flags promptly once the feature is fully shipped — stale flags accumulate as debt.

## Secure boot and OTA update safety

For connected products, treat the boot and update path as a security-critical subsystem.

### Boot chain

- Verify firmware signature before execution at every stage (ROM → bootloader → application).
- Use hardware-rooted trust (OTP fuses, secure element, TrustZone) where the SoC supports it.
- Lock debug ports (JTAG/SWD) in production builds via fuse or APPROTECT.
- Log boot reason (watchdog, brownout, normal, update) for diagnostics.

### OTA updates

- Sign all firmware images cryptographically; reject unsigned or tampered images before writing.
- Use A/B bank (or equivalent dual-image) layout with automatic fallback on boot failure.
- Implement anti-rollback counters to prevent downgrade attacks.
- Verify image integrity (CRC + signature) after write, before marking the bank as active.
- Define and test the recovery path for every update failure mode: power loss mid-write, corrupt download, signature mismatch, bank swap failure.
- Test the full update path on real hardware — simulation alone cannot prove the flash/boot interaction.

### Things to record for boot and update subsystems

- key storage location and provisioning method
- signature algorithm and key rotation plan
- anti-rollback counter location and increment policy
- fallback behavior when both banks are invalid
- factory reset and recovery mode behavior

## Good prompts to encode later as project-specific skills

- "Trace all direct hardware access for this feature and propose a seam."
- "Design a host simulation harness for this module before changing behavior."
- "List the failure modes for this storage path under power loss."
- "Compare RAM, flash, stack, and timing impact before and after the change."
- "Instrument flash erases, writes, and reads behind a seam, assign weights, and reduce the score without changing behavior."
- "Count constructions, copies, moves, and allocations in this C++ path and propose the smallest change that lowers the weighted score."
- "Use the linker map, `size`, or `bloaty` to find the biggest RAM/flash contributors and reduce them without weakening behavior."
