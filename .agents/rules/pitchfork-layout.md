---
paths:
  - "src/**"
  - "include/**"
  - "libs/**"
  - "tests/**"
  - "external/**"
  - "tools/**"
  - "data/**"
  - "extras/**"
---

# Pitchfork C++ Project Layout

This project follows the [Pitchfork C++ project layout](https://vector-of-bool.github.io/2018/09/16/layout-survey.html).

## Directory map

| Directory | Purpose | Required |
|---|---|---|
| `src/` | Source files; private headers (merged placement: public headers here too) | Yes |
| `include/` | Public headers only (separate header placement) | If using separate placement |
| `libs/` | Sub-libraries — each with its own `src/` and optionally `include/` | When sub-libraries exist |
| `tests/` | All test source; mirrors source layout where practical | Yes |
| `external/` | Vendored or submodule third-party dependencies — do not modify directly | When vendoring |
| `tools/` | Build scripts, code generators, CI helpers | When tooling exists |
| `data/` | Static data files: configs, fixtures, calibration tables | When needed |
| `extras/` | Examples, benchmarks, integration demos — not required by the main build | Optional |
| `docs/` | Documentation, ADRs, work packets | Yes |
| `build/` | Build artifacts — not tracked in VCS; add to `.gitignore` | Generated |

## Header placement — choose one and apply it consistently

**Merged placement** (simpler; preferred for single-library firmware):
- Public and private headers alongside source in `src/`
- `#include "module/header.h"` from other modules

**Separate placement** (preferred when the public API is a stable, versioned contract):
- Public headers in `include/<project-name>/`
- Private headers alongside source in `src/`
- Consumers `#include <project-name/header.h>`

## Embedded firmware conventions under Pitchfork

- HAL, BSP, and driver layers are sub-libraries: `libs/hal/`, `libs/bsp/`, `libs/drivers/<name>/`
- Each sub-library follows the same merged/separate rule as the top level
- Platform-specific code lives inside a sub-library, not as a sibling of `src/`
- RTOS port or OS abstraction layer: `libs/os/` or `libs/rtos/`
- Linker scripts, startup files, and vector tables: `src/` or a dedicated `libs/startup/`

## Rules for planner and developer

- When planning a new module, explicitly name which Pitchfork directory each new file goes in before writing any code.
- When creating a file, place it in the correct directory first.
- When a file is already in the wrong directory, flag it as structural debt; fix it in a separate tidy commit before the behavioral change.
- Do not create new top-level directories (`mymodule/`, `common/`, `shared/`) without documenting why Pitchfork does not have a canonical home for the content and getting explicit agreement.
- Do not co-locate test files with source files; tests live in `tests/`.
- Do not place source or header files at the repository root.
- Do not put external dependencies inside `src/` or `libs/`; use `external/`.
