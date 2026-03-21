---
name: hypothesis-driven-debugging
description: Debug by ranking concrete hypotheses and running discriminating checks. Use when a bug is hard to localize, many plausible failure points exist, logs are noisy or misleading, a symptom appears intermittently, or trial-and-error edits haven't worked.
allowed-tools: Read, Grep, Glob, Bash
---

# Hypothesis-Driven Debugging

Find root cause through evidence, not broad trial-and-error edits.

## Tracking convention

Persist the investigation on disk.

- Create or reuse the work packet under `docs/work/<work-id>/`.
- Store one file per hypothesis under `docs/work/<work-id>/evidence/hypotheses/`.
- Name files like `HYP-001-short-title.md`, `HYP-002-timeout-path.md`.
- Use `docs/templates/hypothesis-template.md`.
- Update the file every time you run a discriminating check: what was tested, how it was tested, and the result.

## Process (TRAFFIC)

1. **Track** — capture the exact symptom: error message, stack trace, or observable wrong behavior, reproduction steps, hardware/firmware version. Create or reuse the work packet and start the first hypothesis records immediately.

2. **Reproduce** — confirm the failure triggers reliably. Tighten to the smallest input or sequence that reproduces it. An unreproducible bug cannot be safely fixed.
   ```
   Grep("<error-string>|<symptom-keyword>"), Read("<relevant-log-or-trace>")
   ```

3. **Automate** — write a minimal failing test or script that reproduces the failure before touching production code.

4. **Form hypotheses** — list at least 3 plausible causes, including unlikely ones. Create one file per hypothesis. Ask all three question types for each candidate area:
   - *What* does this component do?
   - *How* does it do it?
   - *Why* was it designed this way?

5. **Focus** — rank hypotheses by likelihood × testability. Design the **cheapest discriminating check** that falsifies at least one hypothesis. Write the planned check into the hypothesis file before running it. Apply binary search / divide-and-conquer: place an assertion or check at the midpoint of suspect code; determine which half contains the defect; recurse.

6. **Investigate** — run the check. Update the hypothesis file with what was tested, how it was tested, the result, and the new confidence. **Do not fix anything yet.** Repeat until one hypothesis explains all observations. For timing-sensitive paths, switch immediately to non-intrusive methods (GPIO + logic analyzer, ITM/SWO trace) rather than breakpoints.

7. **Correct** — fix the root cause identified by the evidence; verify the reproducing test now passes.

## Cognitive guardrails
- **Confirmation bias** is the most damaging derailing force: explicitly ask "What would prove this hypothesis wrong?" and go test that before committing.
- **Availability heuristic**: do not blame the most recently changed component without evidence.
- **Anchoring**: the first plausible explanation is not necessarily the right one; keep the hypothesis list alive.
- Never make code changes until root cause is identified — changes mask evidence.
- Do not treat a hypothesis as confirmed until evidence explicitly supports it.
- Do not keep hypothesis updates only in chat memory; persist them in the work packet.

## Embedded-specific techniques
- **Non-intrusive trace first for timing bugs** — JTAG breakpoints halt execution and change timing; use GPIO toggles + logic analyzer, or ITM/ETM trace instead.
- **Hard fault handler** — on Cortex-M, read stacked LR/PC/PSR to identify the faulting instruction without a JTAG connection.
- **Delta debugging over commits** — `git bisect` applies binary search over commit history to isolate the introducing change.

## When debugging stalls
- **Repro is not reproducible** — add observability (`observability-and-diagnostics`) before continuing.
- **All hypotheses are eliminated** — the symptom description is incomplete; revisit step 1.
- **Root cause requires hardware access** — document what needs to be measured; use simulation to cover the testable portion.
- **Stuck for >30 min** — explain the problem out loud (rubber duck); forced articulation re-examines assumptions.

## Done-when
- root cause is stated clearly
- evidence supports the diagnosis
- the fix addresses that cause
- the hypothesis files show what was tested, how it was tested, and what happened

## Output
- symptom (precise)
- hypothesis files created or updated
- hypotheses considered
- discriminating checks run, how they were run, and results
- root cause
- fix summary
- verification summary
