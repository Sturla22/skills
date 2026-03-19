# Firmware Playbook

Use this as the place to encode repo-specific engineering norms.

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
