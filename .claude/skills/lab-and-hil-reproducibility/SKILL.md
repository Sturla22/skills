---
name: lab-and-hil-reproducibility
description: Make bench, HIL, flashing, and cross-component integration checks reproducible and auditable. Use when hardware identity, fixture setup, flashing steps, artifact capture, flaky-lab triage, or product-versus-environment failure classification need a repeatable workflow.
allowed-tools: Read, Grep, Glob, Bash
---

# Lab and HIL Reproducibility

Turn real-environment testing into repeatable evidence instead of bench folklore.

## Process

1. **Start from the claim and the packet** — read the work packet first so the bench work serves a concrete claim.
   ```
   Read("docs/work/<work-id>/brief.md"), Read("docs/work/<work-id>/plan.md"), Read("docs/work/<work-id>/status.md"), Glob("docs/work/<work-id>/evidence/**")
   ```

2. **Make the setup identity explicit** — record the exact board or device ID, probe, serial path, fixture or wiring, firmware revision, flash command, and relevant tool versions. If shared lab resources are used, note how they are acquired and released.

3. **Write the shortest repeatable setup path** — capture the steps another engineer would need to reproduce the run without oral history: environment variables, flashing steps, power-cycle requirements, expected boot or log markers, and teardown.

4. **Run focused checks and capture durable artifacts** — prefer a narrow set of checks tied to the claim. Persist logs, command invocations, screenshots, traces, or other artifacts under the work packet instead of leaving them only in chat or terminal memory.

5. **Classify each failure honestly** — for every failure, say whether it currently looks like:
   - product defect
   - environment or rig defect
   - unknown

6. **Handle flake as a first-class problem** — if reruns are ambiguous, stop normalizing the flake. Isolate the unstable board, fixture, test, or environment assumption. Quarantine unstable lanes when that preserves signal better than repeated soft passes.

7. **Reduce the next round cost** — recommend setup automation, clearer observability, or a better host-side seam when that would remove the recurring integration bottleneck.

## Guardrails
- Do not call a setup reproducible if key hardware identity or flashing details are missing.
- Do not bury rig instability under a nominal pass.
- Do not keep rerunning the same flaky path without improving the classification signal.
- Do not let screenshots or logs become evidence without recording how they were produced.
- Do not normalize one-off bench heroics as the expected workflow.

## When integration evidence is weak
- **Board identity changes between runs** — record the difference and stop comparing runs as if they were equivalent.
- **Setup steps are too long or implicit** — write a runbook or script for the minimal stable path.
- **Logs are noisy or insufficient** — add focused observability before rerunning.
- **Host testing could answer most of the question** — hand back the seam recommendation instead of spending more time on hardware-only iteration.

## Done-when
- another engineer could repeat the setup from the recorded steps
- hardware and tool identity are explicit
- artifacts are stored durably
- failures are classified honestly
- flaky infrastructure is called out or quarantined

## Output
- setup identity
- repeatable run steps
- checks run
- artifacts gathered
- failure classification
- blockers, instability, or quarantine candidates
- recommended next improvement to reduce bench cost
