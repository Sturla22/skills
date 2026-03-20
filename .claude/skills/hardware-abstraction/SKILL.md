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
   // C++: pure virtual interface (runtime polymorphism)
   class IUart {
   public:
       virtual ~IUart() = default;
       virtual bool init(uint32_t baud) = 0;
       virtual int  send(const uint8_t* buf, std::size_t len) = 0;
   };
   ```

   **Policy-based design (compile-time HAL alternative):** Pass the HAL back-end as a template policy instead of a virtual interface. Zero vtable overhead; the compiler substitutes the policy at build time per target (real hardware, host stub, test mock).
   ```cpp
   // Policy: any type implementing init() and send()
   template<typename UartPolicy>
   class UartDriver : private UartPolicy {   // private inheritance for EBCO
   public:
       bool init(uint32_t baud) { return UartPolicy::init(baud); }
       int  send(const uint8_t* buf, std::size_t len) { return UartPolicy::send(buf, len); }
   };

   // Production build: UartDriver<RealUartPolicy>
   // Host test build: UartDriver<StubUartPolicy>
   ```
   Empty Base Class Optimization (EBCO) applies when the policy carries no data; inheriting privately rather than holding by value keeps `sizeof(UartDriver<StatelessPolicy>) == sizeof(UartDriver<>)`.

   **CRTP (zero-cost driver interface):** Use the Curiously Recurring Template Pattern when a base class needs to call derived-class methods with no virtual dispatch.
   ```cpp
   // Base enforces interface; derived supplies implementation
   template<typename Derived>
   class DriverBase {
   public:
       bool init(uint32_t baud) { return static_cast<Derived&>(*this).do_init(baud); }
       int  send(const uint8_t* buf, std::size_t len) {
           return static_cast<Derived&>(*this).do_send(buf, len);
       }
   private:
       DriverBase() = default;               // private constructor prevents direct use
       friend Derived;                        // friend guard: mismatched template arg → compile error
   };

   class SpiUart : public DriverBase<SpiUart> {
   public:
       bool do_init(uint32_t baud) { /* vendor HAL */ return true; }
       int  do_send(const uint8_t* buf, std::size_t len) { /* vendor HAL */ return len; }
   };
   ```
   Note: C++23 deducing-`this` (P0847) simplifies some CRTP patterns but is unavailable on C++11/14/17 targets common in embedded.

   **Placement new for typed MMIO access:** Overlay a C++ register-accessor type onto a fixed hardware address using placement new instead of a raw `reinterpret_cast`.
   ```cpp
   // Peripheral descriptor type with named register fields
   struct UartRegs {
       volatile uint32_t CR1;
       volatile uint32_t CR2;
       volatile uint32_t DR;
   };

   // Construct the accessor at the hardware base address — no allocation
   alignas(UartRegs) static std::byte mmio_storage[sizeof(UartRegs)];
   auto* regs = new(reinterpret_cast<void*>(0x40011000)) UartRegs{};
   ```
   `volatile` must propagate correctly through every field and pointer; a non-`volatile` pointer to the object allows the compiler to cache reads or elide writes. `std::launder` (C++17) is required for strict standard conformance when accessing the object through the original pointer after placement new; on C++11/14 toolchains this is technically UB but compilers do not miscompile it in practice — note in safety-critical contexts.

5. **Move policy above the boundary** — decision logic, retry policies, and state machines live above the seam; only raw mechanism lives below.

   **RAII for peripheral ownership:** Wrap peripheral acquire/release in RAII guards so the resource is released on every exit path, including early returns and error paths (even in `-fno-exceptions` builds).
   ```cpp
   // SPI bus lock guard
   class SpiBusLock {
   public:
       explicit SpiBusLock(ISpi& spi) : spi_(spi) { spi_.acquire(); }
       ~SpiBusLock() { spi_.release(); }
       SpiBusLock(const SpiBusLock&) = delete;
       SpiBusLock& operator=(const SpiBusLock&) = delete;
   private:
       ISpi& spi_;
   };

   // GPIO peripheral enable/disable guard
   struct GpioClockGuard {
       GpioClockGuard()  { RCC->AHB1ENR |= RCC_AHB1ENR_GPIOAEN; }
       ~GpioClockGuard() { RCC->AHB1ENR &= ~RCC_AHB1ENR_GPIOAEN; }
   };

   // Power-rail guard
   struct PowerRailGuard {
       explicit PowerRailGuard(PowerRail& rail) : rail_(rail) { rail_.enable(); }
       ~PowerRailGuard() { rail_.disable(); }
   private:
       PowerRail& rail_;
   };
   ```
   Apply RAII guards at every peripheral acquisition site: SPI bus locks, GPIO clock enables, DMA channel grants, and power-rail enable sequences are all candidates.

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
- On multi-core or DMA-capable SoCs, `volatile` alone does not guarantee memory ordering; add explicit memory barriers (`DMB`/`DSB` on ARM, or `std::atomic_thread_fence`) for shared MMIO regions accessed by DMA or a second core.

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
