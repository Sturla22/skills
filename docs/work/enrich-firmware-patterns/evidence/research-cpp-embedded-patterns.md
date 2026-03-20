# Research Summary: C++ Embedded Design Patterns

**Work ID:** enrich-firmware-patterns
**Researcher:** researcher role
**Date:** 2026-03-20
**Status:** Complete

---

## Executive Summary

Nine seed patterns are fully covered below, each with definition, when-to-use guidance, key tradeoffs, and at least one authoritative citation. Five additional patterns surfaced from the sources and are included as related entries. Patterns are grouped by natural affinity: concurrency and message-passing primitives (Active Object, ring buffer, command queue), compile-time abstraction techniques (CRTP, policy-based design), heap-free library tooling (ETL), hardware-interface construction (placement new for MMIO), behavioral modeling (state machines), and inter-component signaling (observer / event bus). Gaps where hardware or platform specifics would materially change the answer are flagged at the end of each relevant entry and collected in a Gaps section.

---

## Group 1: Concurrency and Message-Passing Primitives

### 1.1 Active Object (Asynchronous Method Execution via Message Queue)

**Definition.** An Active Object is an independently scheduled object that owns a private event queue and a dedicated execution context (thread or task). Callers post events asynchronously; the object processes them one at a time in run-to-completion (RTC) steps, eliminating shared-state races without requiring mutex locks on the object's own data.

**When to use.** Use when a subsystem (sensor sampler, protocol handler, motor controller) needs to respond to asynchronous stimuli without blocking its callers. Particularly valuable when the subsystem state is complex enough that protecting it with ad-hoc mutexes becomes fragile, or when you need to decouple producers from a slow consumer across RTOS task boundaries.

**Key tradeoffs.**
- Eliminates intra-object race conditions without mutexes, at the cost of requiring callers to post events rather than call methods directly.
- Queue depth must be provisioned at design time; overflow is a hard fault mode that must be handled explicitly.
- Latency becomes queueing latency, not call latency — appropriate for control loops with relaxed deadlines, but not for hard-real-time direct control paths.
- Debugging is harder: the call stack at failure time is inside the object's event loop, not at the poster's call site.
- Composed naturally with hierarchical state machines (HSMs) to describe the object's behavior.

**Authoritative sources.**
- Miro Samek, *Practical UML Statecharts in C/C++: Event-Driven Programming for Embedded Systems*, 2nd ed. (CRC Press, 2008). ISBN 978-0-7503-0611-0. The definitive embedded reference; Chapter 6 covers Active Objects and their RTOS integration.
- state-machine.com Active Object documentation: https://www.state-machine.com/active-object/ (retrieved 2026-03-20). Defines Active Object as "event-driven, strictly encapsulated software objects running in their own threads of control that communicate with one another asynchronously by exchanging events."

**Hardware/platform gap.** Queue discipline and overflow policy are RTOS-specific. FreeRTOS `xQueueSend`, Zephyr `k_msgq_put`, and bare-metal ring buffers each have different blocking and ISR-callable semantics. The pattern itself is RTOS-agnostic; instantiation is not.

---

### 1.2 Ring Buffer / Circular Buffer (Lock-Free and Lock-Based Variants)

**Definition.** A ring buffer is a fixed-capacity FIFO backed by a contiguous array with head and tail indices that wrap modulo capacity. Data is produced into the tail and consumed from the head without moving elements, making push and pop O(1).

**When to use.** Use for ISR-to-task or task-to-task streaming data (UART RX, ADC samples, log records) where bounded memory, predictable latency, and minimal synchronization cost matter. Choose the lock-free SPSC (single-producer / single-consumer) variant when exactly one thread or ISR writes and exactly one reads; use a locked variant for MPMC (multi-producer / multi-consumer) scenarios.

**Key tradeoffs.**

*Lock-free SPSC variant (wasted-slot method):*
- Full detection: `(head + 1) % size == tail`; empty detection: `head == tail`. One slot is wasted to avoid needing a flag.
- No mutex required: the producer writes only to tail, the consumer reads only from head, and on architectures with coherent cache or appropriate `std::atomic` load/store, no locking is needed.
- Restricted to exactly one producer and one consumer; any deviation requires external synchronization or a different structure.
- `boost::lockfree::spsc_queue` provides a wait-free (stronger than lock-free) implementation when the platform provides the needed atomic instructions. If atomics are unavailable, the implementation falls back to spinlocks, which undermine the wait-free claim.

*Lock-based (flag method):*
- Uses a `full` boolean flag to distinguish full from empty when `head == tail`.
- Requires a mutex or critical section for every access; safe for MPMC but adds scheduling jitter.

**Authoritative sources.**
- Embedded Artistry, "Creating a Circular Buffer in C and C++," https://embeddedartistry.com (retrieved 2026-03-20). Covers full/empty detection strategies and the lock-free SPSC wasted-slot approach.
- Boost.Lockfree documentation, `boost::lockfree::spsc_queue`: https://www.boost.org/doc/libs/1_84_0/doc/html/lockfree.html (retrieved 2026-03-20). States the spsc_queue is "a wait-free single-producer/single-consumer queue (commonly known as ringbuffer)."

**Hardware/platform gap.** Lock-free correctness depends on the memory model of the target ISA. On ARM Cortex-M without a data memory barrier (`DMB`), compiler or CPU reordering can violate the SPSC invariant even with `volatile`. Use `std::atomic` with appropriate `memory_order`; do not rely on `volatile` alone for concurrent access.

---

### 1.3 Command Queue / Message-Passing Between Tasks

**Definition.** The Command pattern encapsulates a request (operation + parameters) as a first-class object. A command queue extends this: callers enqueue command objects; a consumer task dequeues and executes them sequentially, decoupling the issuer from the executor in time and thread context.

**When to use.** Use when a task needs to serialize work requests from multiple producers (UI, network, sensor callbacks), when operations need to be logged or replayed, or when undo/redo semantics are required. Naturally pairs with Active Object (the AO's event queue is a command queue), and with ETL's fixed-capacity queue for heap-free operation.

**Key tradeoffs.**
- Decouples producers from the executing thread, enabling safe multi-source dispatch.
- Queue depth must be bounded at compile time in embedded contexts; a full queue requires an explicit drop, block, or error policy.
- Command objects must be copyable or movable into the queue; large payloads increase queue memory cost. Prefer small, flat command structs or index-based references to shared buffers.
- Runtime virtual dispatch (`execute()`) adds a vtable lookup per command; CRTP or ETL message routing can eliminate this at the cost of compile-time type enumeration.
- The Gang of Four *Design Patterns* (Gamma et al., Addison-Wesley, 1994) defines the pattern; the embedded adaptation is to replace heap-allocated command objects with fixed-size structs or ETL message types.

**Authoritative sources.**
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software* (Addison-Wesley, 1994). Command pattern, pp. 233–242.
- ETL message router documentation: https://www.etlcpp.com/message_router.html (retrieved 2026-03-20). Demonstrates CRTP-based non-virtual message dispatch suitable for embedded command queues.

**Related patterns.** Active Object (1.1), ETL (3.1), CRTP (2.2).

---

## Group 2: Compile-Time Abstraction Techniques

### 2.1 Policy-Based Design (Static Polymorphism via Templates as HAL Alternative)

**Definition.** Policy-based design (coined by Andrei Alexandrescu in *Modern C++ Design*, Addison-Wesley, 2001) configures the behavior of a class by parameterizing it with one or more policy types passed as template arguments. Each policy implements a required interface; the host class selects behavior at compile time with no virtual function cost.

**When to use.** Use when a hardware abstraction layer (HAL) or driver needs to support multiple back-ends (real hardware, host-simulation stub, test mock) without runtime cost or virtual dispatch. Policy types are substituted at compile time per build target, giving zero-overhead platform switching. Also useful for configuring algorithms (e.g., checksum strategy, retry policy, log sink).

**Key tradeoffs.**
- Zero runtime cost: no vtable, no branch on policy type. The compiler inlines policy calls.
- Compile-time coupling: all policy types must be known at compile time. Adding a new policy requires recompilation; runtime swapping requires a separate mechanism (e.g., function pointer or `std::function`).
- Error messages for policy violations are template error messages, which are notoriously difficult to read without C++20 concepts or careful `static_assert` wording.
- Empty Base Class Optimization (EBCO) applies when policies carry no data and are used via inheritance rather than composition, reducing size overhead to zero.
- `std::unordered_map<Key, T, Hash, KeyEqual, Allocator>` is the canonical standard library example: Hash and Allocator are policies.

**Authoritative sources.**
- Andrei Alexandrescu, *Modern C++ Design: Generic Programming and Design Patterns Applied* (Addison-Wesley, 2001). ISBN 978-0-201-70431-0. Chapters 1–2 introduce policy classes and the host-class idiom.
- Rainer Grimm, "Policy and Traits," modernescpp.com, 2022-03-13: https://www.modernescpp.com/index.php/policy-and-traits/ (retrieved 2026-03-20).

**Hardware/platform gap.** Policy substitution for HAL means the simulation policy must accurately model peripheral timing and side-effects. If the policy omits hardware-specific behavior (e.g., SPI clock polarity, I2C stretch), host tests will pass while hardware tests fail. Document what each policy does and does not emulate.

---

### 2.2 CRTP (Curiously Recurring Template Pattern) for Zero-Cost Abstractions

**Definition.** CRTP is a C++ idiom where a derived class inherits from a base class that is parameterized with the derived class itself: `class Derived : public Base<Derived>`. The base class accesses derived-class methods via `static_cast<Derived&>(*this)`, achieving compile-time polymorphism without virtual functions.

**When to use.** Use when you need polymorphic interfaces (e.g., a common driver interface for SPI, I2C, UART) with zero runtime overhead, or when the base class needs to call derived-class methods generically (e.g., mixins that add common boilerplate to hardware register classes). ETL's FSM and message router both use CRTP internally.

**Key tradeoffs.**
- No vtable, no dynamic dispatch: call overhead is equivalent to a direct function call or inlined entirely.
- All types must be known at compile time; you cannot store heterogeneous CRTP objects in a container without wrapping or type erasure.
- Mismatching the template argument (e.g., `class Derived : public Base<OtherClass>`) produces undefined behavior, not a compile error, unless a private-constructor + friend guard is added in the base class.
- Code bloat is possible: each instantiation generates separate code, unlike a single vtable dispatch path. This is usually acceptable in firmware but worth monitoring on flash-constrained devices.
- C++23 Deducing `this` (P0847) reduces some CRTP use cases to simpler syntax but does not replace it on C++11/14/17 targets common in embedded.

**Authoritative sources.**
- Jonathan Boccara, "The Curiously Recurring Template Pattern (CRTP)," fluentcpp.com: https://www.fluentcpp.com/2017/05/12/curiously-recurring-template-pattern/ (retrieved 2026-03-20). Covers mechanics, safeguard pattern (private constructor + friend), and static polymorphism use case.
- ETL FSM documentation using CRTP: https://www.etlcpp.com/fsm.html (retrieved 2026-03-20). States that `on_event` functions are "not virtual" because CRTP is used.

**Related patterns.** Policy-based design (2.1), ETL (3.1).

---

## Group 3: Heap-Free Library Tooling

### 3.1 ETL — Embedded Template Library

**Definition.** The ETL (Embedded Template Library) is a header-only, MIT-licensed C++ library by John Wellbelove that provides STL-compatible containers, algorithms, and embedded-specific frameworks — all with compile-time-fixed capacities and no dynamic memory allocation.

**When to use.** Reach for ETL when targeting bare-metal or RTOS environments where the standard library's heap-allocating containers (`std::vector`, `std::queue`, `std::deque`) are prohibited, where RTTI is disabled, or where you need embedded-specific primitives (FSMs, message routing, observers, CRC) with STL-familiar API. It is particularly useful when the project already bans `new`/`delete` globally.

**Key features.**
- `etl::vector<T, N>`, `etl::queue<T, N>`, `etl::map<K,V,N>`: fixed-capacity drop-ins for STL containers.
- `etl::circular_buffer<T, N>`: fixed-capacity circular buffer (single-threaded; concurrent variants require locked wrappers).
- `etl::fsm` / `etl::fsm_state`: CRTP-based event-driven FSM (see 4.1).
- `etl::message` / `etl::message_router`: CRTP-based non-virtual message routing and inter-task messaging (see 1.3).
- `etl::observer` / `etl::observable`: heap-free observer pattern with compile-time observer count limit (see 5.1).
- `etl::variant`: type-safe union capped at eight types (C++03); use `std::variant` (C++17) or ETL's C++11 variant for more.
- CRC8/16/32/64, type-safe enums, `etl::delegate` (zero-allocation callable wrapper).

**Key tradeoffs.**
- Container capacities are fixed at compile time: you must know worst-case sizes up front. Exceeding capacity at runtime emits exceptions or assertions, not silent growth.
- The base queue and circular buffer are not thread-safe; locked variants are provided as wrappers.
- Extensive (10,000+ unit tests) but the library is not formally MISRA-certified. Projects with strict MISRA compliance requirements must audit ETL usage against their subset.
- C++98 compatibility is a strength (wide toolchain reach) but means some modern C++ idioms are expressed in older syntax; the C++11/17 variants are cleaner.

**Authoritative sources.**
- ETL GitHub repository (John Wellbelove, active since 2014): https://github.com/ETLCPP/etl (retrieved 2026-03-20).
- ETL home page: https://www.etlcpp.com/home.html (retrieved 2026-03-20).

---

## Group 4: Hardware-Interface Construction

### 4.1 Placement New for Memory-Mapped Peripherals

**Definition.** Placement new constructs a C++ object at a caller-supplied address without allocating memory: `new(address) T(args)`. For memory-mapped I/O (MMIO), this allows a typed register-accessor object to be overlaid on a fixed hardware address, replacing raw pointer casts.

**When to use.** Use when you want to give a hardware peripheral register block a proper C++ type (with named fields, accessor methods, or invariant checks) while keeping it pinned at the linker-assigned or hardware-specified address. Preferred over `reinterpret_cast<Peripheral*>(address)` alone because it explicitly names the construction site and can invoke a constructor that validates register state.

**Key tradeoffs.**
- The `volatile` qualifier must propagate correctly: the placement target address should be `volatile`-qualified, and all accesses through the resulting pointer must respect `volatile` to prevent the compiler from caching reads or eliding writes to hardware registers.
- `std::launder` (C++17) is required to legally access the resulting object through the original pointer after placement new on some compilers; omitting it is technically UB in strict aliasing interpretations.
- The destructor must be called manually (`ptr->~T()`) before the storage is reused; no RAII wrapper automatically handles this for MMIO-pinned objects.
- Alignment: the supplied address must satisfy `alignof(T)`. Most MMIO peripheral bases are word-aligned, but verify for packed or over-aligned types.
- Passing a null pointer to placement new is undefined behavior.
- This is a niche but legitimate embedded pattern; it is not a general-purpose replacement for `std::make_unique` or standard containers.

**Authoritative sources.**
- cppreference.com, "new expression," https://en.cppreference.com/w/cpp/language/new (retrieved 2026-03-20). Covers placement syntax, alignment, lifetime, null-pointer UB, and `std::launder` interaction.
- Michael Caisse, "Practical `constexpr` for Embedded C++" (CppCon 2018, YouTube). Covers typed MMIO register access patterns including placement new and `volatile`.

**Hardware/platform gap.** Peripheral register layout, endianness, and access-width requirements (byte vs. word vs. doubleword) are chip-specific. A placement-new-constructed peripheral accessor must still match the hardware's access semantics, which requires datasheet verification. Some peripherals require read-modify-write sequences that a simple wrapper may not enforce.

---

## Group 5: Behavioral Modeling

### 5.1 State Machine Patterns (Hierarchical, Table-Driven, std::variant-Based)

**Definition.** A finite state machine (FSM) models object behavior as a set of states, transitions triggered by events, and optional entry/exit actions. Three common implementation strategies in embedded C++ are: (1) flat switch/case or table-driven; (2) hierarchical state machines (HSMs / UML Statecharts); (3) `std::variant`-based with the overload pattern.

**Flat switch/case and table-driven FSMs.**
- Implementation: a `switch` on current state with inner cases per event, or a 2D array `table[state][event] = {next_state, action_fn}`.
- When to use: simple FSMs with few states and no shared behavior. Table-driven is easier to visualize and audit; the table is the specification.
- Tradeoffs: state explosion for complex behavior; no code sharing between states; the table must be kept consistent with the implementation manually.

**Hierarchical State Machines (HSMs / UML Statecharts).**
- Definition: states can be nested; a child state inherits transitions and entry/exit actions from its parent. Events not handled by a child state are passed up to the parent automatically.
- When to use: complex reactive systems with many shared transitions (e.g., a communications protocol with a generic "error" parent state). Miro Samek's QP framework and ETL's FSM both implement HSMs.
- Tradeoffs: significantly more expressive than flat FSMs; eliminates duplicated transition code. Learning curve is steeper; correct hierarchical dispatch requires a framework (manually implementing it correctly is error-prone). ETL's FSM uses CRTP to eliminate virtual `on_event` calls.
- Source: Miro Samek, *Practical UML Statecharts in C/C++* (CRC Press, 2008). The reference text for HSMs in embedded C/C++.

**std::variant-based FSM (C++17+).**
- Definition: each state is a distinct struct; the current state is stored in a `std::variant<State1, State2, ...>`. Events are dispatched via `std::visit` with the overload pattern.
- When to use: when the number of states is small, states have meaningfully different data, and you want the compiler to enforce exhaustive event handling. Works well for protocol or connection-lifecycle FSMs in host-side code or higher-capability MCUs.
- Tradeoffs: `std::variant` requires C++17; it introduces `std::visit` overhead (similar to a virtual call on some implementations). On deeply constrained targets (Cortex-M0, 8-bit), `std::variant` and exceptions may be unavailable or too costly. No built-in hierarchy. ETL's variant (capped at 8 types, C++03-compatible) is an alternative.

**Authoritative sources.**
- Miro Samek, *Practical UML Statecharts in C/C++: Event-Driven Programming for Embedded Systems*, 2nd ed. (CRC Press, 2008).
- ETL FSM documentation: https://www.etlcpp.com/fsm.html (retrieved 2026-03-20).
- Rainer Grimm, "Visiting a std::variant with the Overload Pattern," modernescpp.com: https://www.modernescpp.com/index.php/visiting-a-std-variant-with-the-overload-pattern/ (retrieved 2026-03-20).

**Hardware/platform gap.** HSM entry/exit timing matters in real-time contexts: long entry/exit chains can add latency to event processing. Measure RTC step time under worst-case event sequences on the target before committing to deep hierarchies.

---

## Group 6: Inter-Component Signaling

### 6.1 Observer / Event Bus Without Heap Allocation

**Definition.** The Observer pattern defines a one-to-many dependency so that when one object (the subject / observable) changes state, all registered dependents (observers) are notified automatically. An event bus generalizes this: any component can publish typed events, and any component can subscribe, with the bus routing messages between them without direct coupling.

**When to use.** Use when multiple independent subsystems need to react to the same event (e.g., a voltage measurement triggers both a display update and a protection check). Prefer over direct function calls when the set of subscribers may vary by configuration or when you want the publisher to be unaware of its consumers. Use the ETL observer when the maximum subscriber count is known at compile time and heap allocation is forbidden.

**Key tradeoffs.**
- ETL's `etl::observer` / `etl::observable`: maximum observer count is a template parameter. No heap allocation. Attempting to exceed the limit emits `etl::observer_list_full`. Observers cannot be removed during a notification traversal.
- Virtual notification: ETL's observer `notification()` is pure virtual (unlike the FSM/message router which use CRTP). This simplifies implementation but adds a virtual call per observer notification.
- Event bus variants: a bus with a compile-time type-indexed dispatch (similar to ETL's message router) can eliminate virtual calls but requires all event types to be known at compile time.
- Notification order is deterministic (registration order) but subject to change if observers are dynamically added/removed across threads; external synchronization is required in that case.
- A common embedded pitfall: notifying observers from ISR context. If `notify_observers()` is called from an ISR, every observer's `notification()` must be ISR-safe — usually it is better to post to a queue and notify from task context.

**Authoritative sources.**
- Erich Gamma et al., *Design Patterns: Elements of Reusable Object-Oriented Software* (Addison-Wesley, 1994). Observer pattern, pp. 293–303.
- ETL observer documentation: https://www.etlcpp.com/observer.html (retrieved 2026-03-20).

**Hardware/platform gap.** ISR-safe notification is hardware/RTOS-specific. Whether `notify_observers()` can be called from an ISR depends on whether any observer implementation uses RTOS blocking primitives, which is an application-level guarantee the pattern itself cannot enforce.

---

## Additional Patterns Surfaced by Sources

The following patterns appeared frequently alongside the seed patterns in authoritative sources and are worth flagging for the planner.

### A. Delegate / Callback Wrapper (Zero-Allocation Callable)

ETL provides `etl::delegate`, a type-safe callable wrapper that captures free functions, member functions, or lambdas without heap allocation. It is the embedded analogue of `std::function` but with a fixed, small footprint and no dynamic allocation. Useful wherever a callback is needed (timer callbacks, completion handlers) and `std::function` is too heavy. Source: ETL documentation, https://www.etlcpp.com (retrieved 2026-03-20).

### B. Memory Pool (Fixed-Block Allocator)

A memory pool pre-allocates a fixed number of same-size blocks at startup and dispenses them via acquire/release without heap fragmentation. It underpins heap-free use of patterns that would otherwise allocate (command objects, event objects). ETL provides `etl::pool`. Source: ETL documentation; also discussed in Miro Samek, *Practical UML Statecharts*, Chapter 6 (event pool for Active Objects).

### C. Double Buffer / Ping-Pong Buffer

A pair of fixed buffers where the producer writes to one while the consumer reads from the other, then they swap. Common for DMA-driven ADC, audio, or display pipelines. Eliminates tearing without a ring buffer's head/tail overhead at the cost of doubling memory and requiring explicit synchronization on the swap. Not covered in ETL directly; a pattern documented in real-time DSP and firmware literature. Source: implied by Boost.Lockfree discussion of SPSC ring buffers vs. double-buffer alternatives.

### D. Type Erasure via `etl::imessage` / `etl::ifsm_state`

ETL consistently exposes a non-template base interface (`imessage`, `ifsm_state`, `icircular_buffer`) alongside the template concrete type. This allows code to accept or store heterogeneous instances through the base pointer without knowing the concrete type or using `std::any`. A lightweight embedded form of type erasure that avoids RTTI. Source: ETL documentation across FSM, message, and circular buffer pages (retrieved 2026-03-20).

### E. Resource Acquisition Is Initialization (RAII) for Peripheral Ownership

RAII applied to hardware resources (SPI bus locks, GPIO enable/disable, critical sections, power-rail guards) ensures resources are released even when exceptions or early returns occur. In an exception-free embedded build, RAII still eliminates the class of bugs where a peripheral is left locked or powered on after an error path. Pairs naturally with placement new (4.1) for peripheral lifecycle management. Source: Bjarne Stroustrup, *The C++ Programming Language*, 4th ed. (Addison-Wesley, 2013); widely cited in embedded C++ literature.

---

## Gaps

The following areas would require hardware or platform confirmation before the research conclusions can be applied directly:

1. **Memory ordering for lock-free ring buffers on specific ISAs.** Correct SPSC ring buffer operation requires appropriate `std::atomic` memory ordering (`memory_order_acquire` / `memory_order_release`). ARM Cortex-M3/M4+ have the necessary barriers; Cortex-M0/M0+ lack `LDREX`/`STREX` and may fall back to disabling interrupts. Platform confirmation needed per target.

2. **ETL MISRA compliance.** ETL is extensively tested but not formally MISRA-certified. Teams operating under IEC 62443, ISO 26262, or DO-178C should audit ETL against their applicable MISRA C++:2008 or 2023 subset before adopting it.

3. **std::variant availability on constrained targets.** `std::variant` (C++17) and `std::visit` are available in GCC arm-none-eabi from approximately GCC 7 onwards, but require C++ exceptions or `<variant>` with `-fno-exceptions` workarounds on some toolchains. Confirm toolchain support before using `std::variant`-based FSMs.

4. **Placement new and `std::launder` on older toolchains.** `std::launder` is C++17. Strictly correct placement-new-over-MMIO code on C++11/14 toolchains operates in a gray area of the standard. In practice compilers do not miscompile it, but the formal UB should be noted in safety-critical contexts.

5. **HSM entry/exit timing on hard-real-time systems.** Deep state hierarchies can produce variable-length RTC steps depending on how many state levels are entered or exited. Measuring worst-case execution time (WCET) on the actual target is required before using HSMs in safety-critical timing paths.

6. **Active Object stack and queue sizing.** Stack depth and queue depth for Active Objects are RTOS and application specific. No platform-agnostic rule exists; sizing requires workload analysis per deployment target.

7. **Volatile semantics for MMIO wrappers.** The C++ standard's `volatile` guarantees (no elision, no reordering between volatile accesses) are weaker than what hardware requires on multi-core or DMA-capable SoCs. Memory-mapped peripheral wrappers on such targets may require explicit memory barriers beyond `volatile`. Architecture-specific audit required.

---

## Research Boundary

This document reports publicly documented facts about C++ embedded design patterns, their mechanics, their tradeoffs, and their authoritative sources as of 2026-03-20. It does not prescribe which existing skills should be updated, what new examples should be written, what the update priority order should be, or how much of each pattern belongs in each skill file — those are design and planning decisions that fall to the planner role.
