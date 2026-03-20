---
name: resource-budget-review
description: Review RAM, flash, stack, CPU, latency, and logging impact as part of the change. Use when changing allocation patterns, buffers, queues, or state machines, adding platform features or diagnostics, or moving behavior into a tighter execution context.
allowed-tools: Read, Grep, Glob, Bash
---

# Resource Budget Review

Treat resource use as part of correctness.
If the goal is to actively reduce a specific cost or footprint rather than review overall budgets, pair this with `operation-cost-optimization`.

## Process

1. **Read the change and its context** — understand what is being added, moved, or removed.
   ```
   Grep("malloc|alloc|static|stack|queue|buffer|log|timer|DMA", type="<lang>")
   ```

2. **Identify resource areas touched** — work through the checklist below.

3. **Measure or estimate impact** using the appropriate tool:

   | Resource | Tool | Command |
   |---|---|---|
   | Flash / ROM size | `bloaty` (diff) | `bloaty new.elf -- old.elf` |
   | Section totals | `size` | `arm-none-eabi-size firmware.elf` |
   | Per-symbol size | `nm` | `arm-none-eabi-nm --size-sort --print-size firmware.elf` |
   | Stack depth (static) | `puncover` | build with `-fstack-usage`, run `puncover` |
   | Stack watermark (runtime) | FreeRTOS API | `uxTaskGetStackHighWaterMark(task)` |
   | CPU usage per task | FreeRTOS stats | `vTaskGetRunTimeStats(buf)` (enable in FreeRTOSConfig.h) |
   | Power / current | Joulescope / PPK2 | correlated with GPIO state markers |

4. **Compare to known budgets** — check linker region limits, RTOS task stack sizes, documented CPU ceilings (~60–70% max utilization under RMS).

5. **Flag hotspots and unknowns** — note anything requiring measurement before the change ships. Estimates are acceptable when measurement is impractical, but must be labeled as estimates.

## Review checklist
- **Stack growth** — especially in ISR or recursive paths; static analysis via `-fstack-usage` + `puncover`; never use recursion in safety-critical code without bounded depth
- **RAM and flash impact** — `.text` (flash), `.bss`/`.data` (RAM); track with `bloaty` diff in CI
- **CPU cost and jitter** — cycles per call, worst-case path; ISRs doing heavy work must be deferred to tasks via queues
- **Blocking time and latency** — mutex holds, busy-wait, DMA wait; avoid blocking APIs in high-priority tasks
- **Logging overhead** — bytes per event, frequency, storage impact; deferred/TRICE-style logging for hot paths
- **Power / battery implications** — measure active vs sleep current; GPIO-marked waveforms on Joulescope/PPK2
- **Memory pool (fixed-block allocator)** — account for fixed acquire/release overhead on every allocation path; block size must cover the worst-case object size across all users; check `etl::pool` capacity against worst-case concurrent acquisition count; verify pool is not exhausted under peak concurrency
- **Double buffer / ping-pong buffer** — double-buffer RAM cost is 2x the single-buffer size; swap synchronization overhead must be accounted for; DMA alignment requirements apply to both buffers independently
- **Active Object queue depth and task stack depth** — queue depth and task stack depth are first-class resource review items; size by workload analysis on the deployment target; no platform-agnostic rule exists — cross-reference `simulation-harness-first` for workload-sizing guidance

## CI enforcement pattern
```bash
bloaty new.elf -- baseline.elf --csv   # fail build if .text grows > budget threshold
```
Add a linker script region size to hard-fail the build on overflow.

## Guardrails
- Do not approve a change that exceeds a known budget without explicit sign-off.
- Do not defer resource review to "after the feature works" — it is part of done.
- If `puncover` reports a worst-case stack depth exceeding the RTOS task stack size, treat it as a build-blocking defect.

## When review is blocked
- **No linker map available** — flag as gap; recommend adding a size report to the build.
- **Budget is undocumented** — document the current baseline; flag the absence of a formal budget.
- **Change is speculative** — do a worst-case estimate; note assumptions explicitly.

## Done-when
- likely resource impacts are stated
- measurements or estimates are recorded
- hotspots or unknowns are visible

## Output
- resource areas touched
- expected impact (measured or estimated)
- tool outputs (bloaty diff, puncover worst-case stack, CPU stats)
- unknowns and follow-up checks
