---
name: observability-and-diagnostics
description: Add or refine the minimal logs, counters, asserts, and traces needed to verify and support the system. Use when a bug is hard to localize, a migration needs confidence signals, failures are silent or ambiguous, or adding observability before a risky change.
allowed-tools: Read, Grep, Glob, Bash
---

# Observability and Diagnostics

Make the system diagnosable without drowning it in noise.

## Process

1. **Find existing diagnostics** — locate current logs, asserts, counters, and trace points near the area of interest.
   ```
   Grep("log_|LOG_|assert|ASSERT|counter|trace|diag|RTT|printf", type="<lang>")
   ```

2. **Identify gaps** — list the boundaries and state transitions that have no signal. Ask: "if this module misbehaves in the field, what will I be able to see?"

3. **Add minimal signals** — one of four types, chosen by the nature of the event:

   | Signal | Use when | Never use for |
   |---|---|---|
   | **Assert** | Invariant violated — indicates a *programmer bug* (null ptr, invalid state transition, impossible enum value) | Hardware-sourced data, recoverable errors, conditions during boot where a reboot loop is possible |
   | **Log (error/warn)** | Expected but exceptional runtime condition needing investigation | High-frequency events (use a counter instead) |
   | **Counter/metric** | Condition occurs regularly and is statistically meaningful at fleet scale | One-off events worth a dedicated log line |
   | **Breadcrumb** | Lightweight "this happened" stamp before a potential crash, stored in NVM | High-frequency events |

4. **Apply the noise rules:**
   - Prefer counters over repeated log lines for high-frequency events.
   - Never call `printf` or blocking UART in ISRs — use deferred capture or TRICE-style ID logging (~6 clock cycles, no format string on device).
   - Compile-time level gating is mandatory: debug logs must generate zero code in production builds.
   - Include units and identifiers in log messages: `net rssi=-72 ssid=Home err=-55`, not `"connection failed"`.

5. **Persist fault context** — always write fault context (PC/LR, fault type, reset count) to NVM before any reset. The last log before a crash is the most valuable.

6. **Verify usability** — confirm the signals are readable in the output format used for debugging (RTT, serial, trace buffer, Memfault coredump).

## Embedded observability tools
- **SEGGER RTT** — communicates over existing SWD/JTAG; ~500 bytes ROM; <1 µs per output; non-blocking (drops if host not reading); safe for all paths.
- **SEGGER SystemView** — records RTOS task switches, ISR entries/exits, and user events; <1% CPU overhead; invaluable for priority inversion, task starvation, missed deadlines.
- **Memfault** — packages coredumps, reboot tracking, asserts, heartbeat metrics, and breadcrumbs for async upload over any transport.
- **TRICE** — macros emit only a 16-bit ID + parameters (~6 clocks, <1 KB total code); format strings live in a host-side JSON dictionary; safe in ISRs.

## Assert philosophy for production firmware
- Do **not** disable asserts in production — redirect the handler to: disable interrupts, save PC/LR to NVM, reset.
- Use compact PC/LR capture (not filename strings) to enable aggressive coverage without code bloat.

## Guardrails
- Do not add logs that expose sensitive data (keys, raw payloads) without redaction.
- Do not add diagnostics that cannot be kept enabled in production without unacceptable overhead.
- Blocking log transports (UART TX full, flash write latency) must be non-blocking with drop detection; count drops as a metric.

## When diagnostics are insufficient
- **Output format is inaccessible** — fix the output channel before adding more signals.
- **Hot path cannot be logged** — use a ring buffer, RTT, or TRICE; flag overhead cost.
- **Signals are insufficient to localize the bug** — apply `hypothesis-driven-debugging` to decide what additional signal is needed.

## Done-when
- important failure boundaries have signals
- diagnostics are cheap enough to keep enabled in production
- verification can use the signals meaningfully

## Output
- diagnostics added or proposed (type, location, rationale)
- why each signal exists
- expected usage in verification and field support
