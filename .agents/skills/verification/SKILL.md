---
name: verification
description: Prove that the claimed change works and state clearly what remains unverified. Use when a code change was made, a bug fix is claimed, a refactor or migration needs evidence, or before marking work as done.
allowed-tools: Read, Grep, Glob, Bash
---

# Verification

Demonstrate the main claim and relevant regressions as far as practical.

Preferred strategy:
- start from behavior scenarios, not implementation guesses
- exercise those scenarios at the lowest sensible level in the test pyramid
- use host simulation before target hardware when hardware is not essential to the claim

## Verification vs. Validation
- **Verification** — "Are we building the product right?" Spec conformance, correctness, ongoing from day one.
- **Validation** — "Are we building the right product?" User needs, fitness for purpose, at milestones or release.

This skill is about verification. Do not conflate passing tests with satisfying user needs.

## Process

1. **Read the change** — understand what was changed and what the claim is.
   ```
   Read("<changed-files>"), Grep("<changed-symbol>")
   ```

2. **Restate the claim, behavior scenarios, and requirement trace** — one sentence for the main claim, then the key observable behaviors and requirements being checked.

3. **Apply the cheapest technique that can detect the relevant defect class:**

   | Defect class | First tool |
   |---|---|
   | Type errors, undefined behavior, null dereferences | Static analysis (`clang-tidy`, `cargo clippy`, `ruff`) |
   | Business logic correctness | Unit tests |
   | Component interaction / API contracts | Integration tests |
   | User-facing workflows | E2E / acceptance tests |
   | Hardware timing, interrupt behavior | On-target / HIL testing |
   | Coding standard compliance | MISRA static analysis |

4. **Run focused checks first** — test the specific behavior claimed, then broader regression suite. Follow the test pyramid: unit (70%) → integration (20%) → E2E (10%). Favor simulation-first host checks before HIL when the claim does not depend on real hardware.

5. **Check acceptance criteria and requirement trace** — match results against the done-when from the plan or task. Acceptance criteria must be concrete and measurable; no "should be fast". Note which requirement or stakeholder need each check does and does not cover.

6. **Check compatibility and release claims** — if the work claims `PATCH`, `MINOR`, `MAJOR`, deprecation-only, or no release impact, compare that claim with the observed contract change and documentation updates such as `CHANGELOG.md`.

7. **State validation gap separately when relevant** — if the change has a stakeholder-fit question, note whether validation evidence or a validation plan exists. Do not confuse a missing validation plan with failed verification, but do not hide the gap either.

8. **State residual risk** — be explicit about what was not verified and why. Residual risk must be stated honestly, not minimized.

## Guardrails
- Do not claim verified without having run an actual check — reasoning alone is not verification.
- Do not suppress or skip failing tests to ship — fix them or document them as known issues.
- If the check environment is broken (flaky tests, missing device), fix it first or flag it explicitly.
- High line coverage with weak assertions gives false confidence — coverage is a floor, not a ceiling.
- Do not accept a non-breaking release classification if the observable contract changed incompatibly.
- Do not claim product fit or stakeholder acceptance from verification evidence alone.

## Common verification gaps to check
- No behavior scenarios — tests exist, but it is unclear which user-visible behavior they prove.
- No static analysis in CI — whole classes of UB and memory errors go undetected.
- Only happy-path tests — error paths and boundary conditions not exercised.
- Missing integration seam tests — two modules' boundary (serialization format, protocol) never tested in isolation.
- Inverted pyramid — too much reliance on slow end-to-end or hardware tests, too little fast deterministic coverage.
- No HIL for embedded — all tests on host; timing and interrupt bugs only appear in the field.
- Acceptance criteria written after implementation — validation theater, not verification.
- No visible requirement trace — checks ran, but it is unclear which need or requirement they actually cover.
- No validation plan on a stakeholder-facing change — implementation may be correct while fitness remains unproven.

## When verification is blocked
- **Tests are flaky** — isolate the flaky test; flaky passes provide no evidence.
- **No automated tests cover the claim** — add a test (see `tdd`) or manually verify and document the steps reproducibly.
- **Hardware is required** — note which claims are hardware-verified and which are host-side only.

## Done-when
- the main claim is demonstrated
- relevant regressions were checked
- requirement coverage is explicit enough to understand the evidence
- compatibility or release claims were checked when relevant
- limitations are stated honestly

## Output
- claim verified (one sentence)
- behavior scenarios checked
- requirement / stakeholder-need coverage
- checks run (type, scope, pass/fail)
- results
- compatibility / release-impact check
- validation gap note when relevant
- residual risk
- not verified (and why)
- verdict
