# AGENTS.md

This repository uses a **roles over skills** model.

## Role boundaries

- **planner** owns task framing, sequencing, constraints, and acceptance criteria
- **developer** makes the smallest effective code change
- **verifier** decides whether the change is actually demonstrated
- **reviewer** looks for hidden risk, overengineering, and missing evidence
- **firmware-architect** protects interfaces, HAL boundaries, migration shape, and long-term structure

Keep one active owner at a time. Prefer explicit handoffs over implicit shared state.

## Embedded firmware defaults

- Prefer **simulation, host tests, and characterization** before hardware-only debugging when practical.
- Keep **hardware access behind narrow interfaces**.
- Make **timing, units, ownership, and failure behavior explicit**.
- Treat **resource use** as part of correctness: stack, RAM, flash, CPU, latency, watchdog behavior, and logging overhead.
- Treat **reboot, timeout, partial-write, corrupt-input, missing-device, and stale-data** scenarios as first-class cases.
- Do not assume a behavior is safe merely because it "usually works on the bench."

## Standard handoff contract

Every handoff should include:

1. Goal
2. Scope
3. Constraints
4. Assumptions
5. Evidence gathered so far
6. Open risks
7. Requested next action
8. Done-when criteria

Use `templates/handoff-template.md`.

## Default skill sequences

### Feature work
1. `codebase-exploration`
2. `planning`
3. `interface-contract-design`
4. `simulation-harness-first`
5. `tdd`
6. `verification`
7. `resource-budget-review`
8. `docs-adr-updates`

### Bug work
1. `codebase-exploration`
2. `hypothesis-driven-debugging`
3. `simulation-harness-first`
4. `tdd`
5. `verification`
6. `fault-injection-and-recovery`

### Design cleanup
1. `codebase-exploration`
2. `simplify-without-behavior-change`
3. `refactoring`
4. `verification`

### Platform migration
1. `codebase-exploration`
2. `planning`
3. `firmware-migration`
4. `hardware-abstraction`
5. `verification`
6. `safety-risk-scan`
7. `resource-budget-review`

## Behavioral defaults

- Do not widen scope silently.
- Do not claim success without evidence.
- Do not replace a concrete requirement with abstraction unless it clearly reduces complexity.
- Prefer **remove before add**, **inline before abstract**, **merge before split**, and **specialize before generalize**.
- State what was not tested on real hardware.
- When uncertain, reduce the next step and add instrumentation.
