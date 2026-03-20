---
name: simulation-harness-first
description: Bias toward deterministic host-side simulation and fake time / I/O before hardware-only iteration. Use when debugging is slow on hardware, logic mixes hardware interaction and decision-making, you need characterization before refactor, or you want fast deterministic test feedback. This is the preferred execution path for lower-level behavior scenarios in the test pyramid when hardware is not required.
allowed-tools: Read, Grep, Glob, Bash
---

# Simulation Harness First

Create a fast, deterministic feedback loop for behavior that does not truly require target hardware.

## Process

1. **Identify what is simulatable** — read the target module and separate hardware-dependent from pure logic.
   ```
   Grep("GPIO|SPI|I2C|UART|HAL_|time_get|sleep|rand|volatile"), Read("<target-module>")
   ```

2. **Introduce seams** — add thin interfaces for time, I/O, storage, and transport so each can be independently faked.

3. **Implement test doubles** — choose the right type per dependency:

   | Type | Use when | Example |
   |---|---|---|
   | **Stub** | Non-critical call; just needs to not crash | `uart_init()` returning `HAL_OK` |
   | **Fake** | Need realistic internal state | RAM-backed flash; FreeRTOS queue in RAM |
   | **Mock** | Need to verify calls, order, or parameters | `spi_transfer_ExpectAndReturn(buf, len, HAL_OK)` |
   | **Spy** | Need to record calls for later assertion | Records every GPIO toggle |

   **Active Object test double.** Fake an Active Object's private queue as a synchronous call in host tests: the caller posts a message; the fake drains the queue immediately in the same thread; the real RTOS task is replaced by the test runner. This removes concurrency from the test while preserving the AO's message-dispatch logic.
   > "Queue depth and task stack depth for Active Objects are workload-dependent; no platform-agnostic rule exists — size by workload analysis on the deployment target."

   **Command queue / message-passing fake.** When faking a bounded command queue, enforce capacity in the double. Example skeleton:
   ```cpp
   struct FakeCommandQueue {
       static constexpr std::size_t CAPACITY = 8;
       std::array<Command, CAPACITY> buf{};
       std::size_t count = 0;

       bool post(const Command& cmd) {
           // Overflow policy must be explicit: drop, assert, or block.
           assert(count < CAPACITY && "FakeCommandQueue overflow — increase CAPACITY or check sender rate");
           buf[count++] = cmd;
           return true;
       }
       Command drain_one() { assert(count > 0); return buf[--count]; }
   };
   ```
   Document the chosen overflow policy (drop / assert / block) in the fake's header comment; an undocumented policy hides behavioral assumptions from readers.

4. **Fake time explicitly** — inject a clock seam instead of calling a global tick function:
   ```cpp
   class IClock {
   public:
       virtual ~IClock() = default;
       virtual uint32_t getTicks() const = 0;
   };
   ```
   In tests, pass a `FakeClock` that implements `IClock`; call `fakeClock.advance(500)` to simulate 500 ms instantly — no `sleep()`, no race conditions.

5. **Capture current behavior with deterministic fixtures** — write tests that exercise the core logic through the fakes and record actual output. Prefer using BDD-style behavior scenarios as the fixture source.

6. **Use the harness for debugging, BDD, and TDD** — reproduce bugs, drive new behavior, and execute lower-level behavior scenarios without hardware.

## Tooling options
- **GoogleTest + GMock** — idiomatic C++ unit testing and mocking; define mocks with `MOCK_METHOD`; integrate with CMake via `FetchContent`. Run `ctest --output-on-failure`.
- **Catch2** — header-only C++ framework with BDD-style `SCENARIO`/`GIVEN`/`WHEN`/`THEN` macros; low setup cost for new projects.
- **QEMU** — boots unmodified firmware ELF on a virtual board; `qemu-system-arm -machine mps2-an385 -kernel firmware.elf`; attach GDB via `-s -S`; pipe results via semihosting.
- **Renode** — multi-board simulation with Robot Framework integration; supports Zephyr, FreeRTOS, multi-node CAN/UART/SPI topologies; GitHub Action available.
- **ETL (Embedded Template Library)** — `etl::queue<T,N>` and `etl::circular_buffer<T,N>` provide compile-time-fixed containers that eliminate heap allocation in test doubles; use them as the backing store in fakes when the production code uses ETL containers. "ETL is not formally MISRA-certified; audit against your applicable MISRA C++ subset before adopting in safety-critical contexts."

## Recommended directory structure
```
hal/
  IUart.hpp           # Interface (seam, pure virtual)
  UartReal.cpp        # Production (vendor HAL calls)
  UartFake.hpp/.cpp   # Test double (stateful fake or GMock)
tests/
  fakes/              # Stateful test doubles (e.g. FakeFlash backed by std::array)
  mocks/              # GMock-derived doubles
  src/                # Test files
```

## Hierarchical State Machine (HSM) testing
Drive HSM event dispatch from a synchronous test loop: post events one at a time and assert on observable state transitions after each dispatch call. Replace the RTOS task-wait with a direct `dispatch()` call in the test runner. This keeps tests deterministic and removes scheduling noise.
Note: RTC (run-to-completion) step timing is invisible in simulation — deep state hierarchies with long entry/exit chains may produce variable-length execution windows on the target. Measure worst-case RTC step timing on the actual target before committing to deep hierarchies in timing-sensitive paths.

## Guardrails
- Fakes must be simple and deterministic — do not model hardware imperfections unless the test requires it.
- Do not let the simulation harness grow into a full hardware emulator — keep it scoped to what the tests need.
- Document which behaviors are covered by simulation and which require target hardware.
- Reset fake state in `setUp()`; assert all expected calls were made in `tearDown()`.

## When harness creation is blocked
- **Seams cannot be introduced** — apply `hardware-abstraction` first.
- **Behavior is too tightly coupled to hardware timing** — document as hardware-only test; note in output.
- **No test infrastructure exists** — start with a single `main()` driver rather than a full test framework.

## Done-when
- the core behavior can be exercised without target hardware
- deterministic repros exist for the relevant scenarios

## Output
- what is simulated
- seams introduced
- test doubles implemented (type and rationale)
- behaviors covered
- hardware-only gaps
