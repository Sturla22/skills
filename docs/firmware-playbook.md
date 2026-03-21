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
- the target graph is visible enough to enforce a small architecture policy at configure time

Use [`extras/cmake-nrf52840-template/`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template) as the concrete starting point when you want a copyable embedded CMake baseline.

## Strong defaults

- Name interfaces in terms of **capabilities**, not vendor details, when the abstraction is intended to survive platform migration.
- Keep **policy** separate from **mechanism**.
- Prefer **pure or mostly pure decision logic** above the HAL boundary.
- Keep **units, ownership, timing, and error semantics** obvious.
- Prefer **deterministic tests** over log-reading as the primary proof.
- When optimizing, count expensive indirect operations behind a seam or measure direct RAM/flash footprint explicitly, then compare before/after results instead of guessing.

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

## Good prompts to encode later as project-specific skills

- "Trace all direct hardware access for this feature and propose a seam."
- "Design a host simulation harness for this module before changing behavior."
- "List the failure modes for this storage path under power loss."
- "Compare RAM, flash, stack, and timing impact before and after the change."
- "Instrument flash erases, writes, and reads behind a seam, assign weights, and reduce the score without changing behavior."
- "Count constructions, copies, moves, and allocations in this C++ path and propose the smallest change that lowers the weighted score."
- "Use the linker map, `size`, or `bloaty` to find the biggest RAM/flash contributors and reduce them without weakening behavior."
