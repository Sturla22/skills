# TDD — Embedded Reference

Supplementary idioms and guardrails for embedded-specific TDD patterns.
The main workflow lives in [SKILL.md](SKILL.md).

## Ring buffer / SPSC

TDD idiom: test producer/consumer separation by exercising the buffer with one writer and one reader double; assert full/empty detection at boundary conditions (capacity, capacity−1, and 0 elements).

Guardrail: lock-free SPSC ring buffer correctness requires `std::atomic` with `memory_order_acquire`/`memory_order_release`; `volatile` alone is insufficient. On Cortex-M0/M0+ without `LDREX`/`STREX`, disable interrupts instead of relying on lock-free atomics.

## Table-driven FSM

TDD idiom: one test per row of the transition table; a missing row is a test failure; table consistency must be maintained alongside tests. The table is the specification — any undocumented transition that passes in production is a latent defect.

## `std::variant`-based FSM

TDD idiom: `std::visit` with the overload pattern makes exhaustive event handling a compile-time check; write a test that verifies unhandled event types fail to compile (use a `static_assert` or a deliberately incomplete overload set that triggers a compile-time error).

Toolchain note: `std::variant`-based FSMs require C++17; confirm toolchain support and `-fno-exceptions` configuration before using on constrained targets.
