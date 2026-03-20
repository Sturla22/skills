---
name: hardware-abstraction
description: Keep direct hardware access behind a narrow seam and separate policy from mechanism. Use when application code touches peripherals directly, platform migration is underway, host simulation is blocked by missing seams, or hardware details are leaking into business logic.
allowed-tools: Read, Grep, Glob, Bash
---

# Hardware Abstraction

Prevent hardware-specific details from leaking into higher-level logic.

## Process

1. **Find direct hardware touch points** — locate all register writes, peripheral calls, and vendor SDK usage.
   ```
   Grep("GPIO|SPI|I2C|UART|HAL_|__asm|MMIO|volatile|DMA", type="<lang>")
   ```

2. **Design the interface top-down** — write the application code you *wish* you could write first; let that drive the interface. Do not mirror the hardware register map; express capabilities the application needs (e.g., `uart_send`, `gpio_set_status_led`).

3. **Define a narrow capability-oriented boundary** — one header per peripheral type; each function maps to exactly one hardware capability. Thin HAL: no business logic, retry policies, or protocol parsing inside the HAL.

4. **Implement with opaque handles** — application code receives a handle it cannot inspect; hardware register details are hidden by the type system.
   ```cpp
   // C++: pure virtual interface
   class IUart {
   public:
       virtual ~IUart() = default;
       virtual bool init(uint32_t baud) = 0;
       virtual int  send(const uint8_t* buf, std::size_t len) = 0;
   };
   ```

5. **Move policy above the boundary** — decision logic, retry policies, and state machines live above the seam; only raw mechanism lives below.

6. **Write the mock alongside the real driver** — the mock is a first-class artifact; if not written now it rarely gets written later.
   ```
   hal_uart_real.c  (production: vendor HAL calls)
   hal_uart_mock.c  (tests: records calls, returns configurable values)
   ```

7. **Create a host-side fake or simulation seam** — implement a host-side fake of the interface for use in tests and simulation harness. Application source is identical in both production and test builds.

## What belongs in a HAL / what does not

| In HAL | Not in HAL |
|---|---|
| Init, read, write, transfer for one peripheral | Business logic, protocol framing, algorithms |
| Error/status return codes | Logging, diagnostics, retry loops |
| Opaque register interaction | Exposed register addresses or bit-field constants |
| Runtime I/O operations | System-level init (clock tree, power sequencing) — that belongs in BSP |

## Guardrails
- Never call hardware registers from an application module — if a module calls `*(volatile uint32_t*)0x40020014`, it cannot be unit-tested on the host.
- Do not let vendor types leak through the boundary into application code.
- Keep the interface to ~12 functions or fewer; extensions go in separate optional headers.
- Avoid `#ifdef TEST` in application business logic — that is a sign the abstraction is incomplete.
- Do not use vendor HAL (STM32Cube, ESP-IDF, Nordic SDK) as the project's HAL — wrap it; don't let application code call it directly.

## When abstraction is difficult
- **Too many callers** — apply `tidy-first` to consolidate callers before introducing the seam.
- **Vendor SDK is deeply embedded** — introduce a thin shim layer first; refactor incrementally using the Strangler Fig pattern.
- **Boundary is unclear** — use `interface-contract-design` to define the contract before writing code.

## Done-when
- hardware touches are localized
- the boundary is explicit and capability-oriented
- higher-level logic is testable on host via the mock

## Output
- touch points found
- abstraction boundary (interface header)
- responsibilities above vs below
- mock/fake implementation
