---
name: tdd
description: Drive implementation with a failing test, the smallest passing change, and safe cleanup. This is the default for product development work. It is optional for non-productized tools when the plan explicitly chooses a lighter-weight verification path.
allowed-tools: Read, Grep, Glob, Bash
---

# TDD

Use tests as the executable spec for the next small behavior change.

TDD is the implementation loop. Use `bdd` to define the behavior and shared language first when the behavior is not already crisp.

## Policy

- Product development follows TDD by default.
- Non-productized tools do not require TDD by default, but they still require explicit verification.
- If a tool is likely to become shared, long-lived, user-facing, or safety-relevant, prefer treating it like product development and use TDD.
- Prefer BDD-style behavior scenarios and names even when tests are not written in formal Given/When/Then syntax.
- Prefer the bottom of the test pyramid first: unit or host-simulation tests before broader or hardware-only checks when the claim allows it.

## Process (Canon TDD — 5 steps)

1. **Write a behavior list** — brainstorm behavioral scenarios and edge cases before writing any test. Add newly discovered cases to the list during development; pick from it deliberately. One test at a time.
   - Prefer BDD-style behavior statements or Given/When/Then notes as the source for the next test.

2. **Read the area under test** — understand the existing API, types, and test conventions before writing a test.
   ```
   Glob("**/{test,tests,spec}/**"), Read("<target-module>"), Read("<test-file>")
   ```

3. **Write one failing test** — express one behavior as the smallest possible assertion. Write the hypothesis down (what you expect to see) before running anything.
   - Name tests as behavioral statements: `Delivery_with_a_past_date_is_invalid()` — not `TestDelivery_ReturnsTrue()`.
   - If the name requires "and", split it into two tests.
   - Place the test at the lowest sensible level in the test pyramid.

4. **Confirm failure for the expected reason** — a test that passes before the fix provides no confidence; wrong failure reason means the test is not testing what you think.

5. **Make it pass** — choose a strategy:
   - **Obvious Implementation** — if you know the solution, code it directly. If it causes an unexpected red, back up and fake it.
   - **Fake It Till You Make It** — return a hard-coded constant first; gradually replace constants with variables.
   - **Triangulation** — write a second specific test that the fake can't satisfy; abstract only when you have two examples.

6. **Refactor only while green** — rename, extract, simplify; re-run after each move. Never refactor in the same step as making a test pass (red → green → refactor are separate mental modes).

## Three laws (nano-cycle — enforced second by second)
1. No production code without a failing test.
2. No more test than is sufficient to fail (including compile failure).
3. No more production code than sufficient to make the currently failing test pass.

## Guardrails
- One failing test at a time — do not accumulate failing tests.
- Do not skip the "confirm failure" step.
- Do not refactor in the same step as making a test pass — the two-hats rule applies here too.
- If writing a test is painful, that is a design signal — the production code may need simplification first.
- Never make private methods public to test them directly — test through the public interface.
- If you are skipping TDD because the work is a non-productized tool, say so explicitly and define the replacement verification approach.

## TDD anti-patterns to avoid
- **The Liar** — test passes but doesn't verify what it claims (assertion always true).
- **The Giant** — one test with 10+ assertions; split into focused single-behavior tests.
- **The Slow Poke** — tests take seconds each; budget ~3 ms per unit test; I/O and sleep calls in unit tests break the feedback loop.
- **Testing Internals** — asserting on private state rather than observable behavior.
- **No Refactor Phase** — skipping the third step produces messy internals even with full coverage.

## Embedded-specific
- All hardware dependencies must be behind a seam (HAL interface) before TDD is possible at unit level.
- Use `simulation-harness-first` to introduce seams if they don't exist yet.
- Prefer running executable behavior scenarios in host simulation before on-target checks when the claim does not depend on real hardware.
- `git bisect` applies binary search over commit history to isolate a regressing commit.

### Ring buffer / SPSC
TDD idiom: test producer/consumer separation by exercising the buffer with one writer and one reader double; assert full/empty detection at boundary conditions (capacity, capacity−1, and 0 elements).

Guardrail: "Lock-free SPSC ring buffer correctness requires `std::atomic` with `memory_order_acquire`/`memory_order_release`; `volatile` alone is insufficient. On Cortex-M0/M0+ without `LDREX`/`STREX`, disable interrupts instead of relying on lock-free atomics."

### Table-driven FSM
TDD idiom: one test per row of the transition table; a missing row is a test failure; table consistency must be maintained alongside tests. The table is the specification — any undocumented transition that passes in production is a latent defect.

### `std::variant`-based FSM
TDD idiom: `std::visit` with the overload pattern makes exhaustive event handling a compile-time check; write a test that verifies unhandled event types fail to compile (use a `static_assert` or a deliberately incomplete overload set that triggers a compile-time error).

Toolchain note: "`std::variant`-based FSMs require C++17; confirm toolchain support and `-fno-exceptions` configuration before using on constrained targets."

## Failure Classification

When a test run does not go as expected, classify before retrying:
- **Wrong failure reason** — test fails but for a different reason than expected; the test is not testing the target behavior. Rewrite the assertion.
- **Environment failure** — build errors, missing dependencies, or broken test runner; fix the environment before writing more tests.
- **Regression** — a previously passing test now fails; the production change broke existing behavior. Revert or narrow the change.
- **Flaky test** — test passes sometimes, fails sometimes; isolate with a deterministic fixture before continuing.

## Done-when
- desired behavior is covered
- failure was observed before the fix
- relevant tests pass

## Output
- failing behavior pinned down
- tests added or changed
- implementation summary
- proof that tests pass
