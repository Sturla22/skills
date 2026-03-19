---
name: interface-contract-design
description: Define stable module contracts with explicit inputs, outputs, failure modes, timing, and ownership. Use when introducing or changing a module boundary, reshaping a HAL or service interface, stabilizing a module before refactor or migration, or resolving ambiguity between callers and implementers.
allowed-tools: Read, Grep, Glob, Bash
---

# Interface Contract Design

Define a contract that can survive implementation changes and platform migration.

## Process

1. **Read existing callers and implementations** — understand what is actually used today.
   ```
   Grep("<interface-name>|<function-name>"), Read("<header-or-trait-file>")
   ```

2. **Draft the contract** — for each function or message, make all ten fields explicit:
   - **Preconditions** — what must be true before calling (inputs, system state, locks held)
   - **Postconditions** — what is guaranteed after a successful return (outputs, changed state, error codes)
   - **Side effects** — what external state changes; what does not change
   - **Ownership** — who owns resources before and after the call; who is responsible for release
   - **Interface authority** — who owns changes to this contract and who must adapt if it changes
   - **Error contract** — which conditions return errors (caller-detectable failures) vs. trigger assertions (programmer bugs)
   - **Concurrency / reentrancy** — thread-safe? ISR-safe? which locks are assumed held?
   - **Timing / real-time constraints** — worst-case execution time, latency bounds, deadline requirements
   - **External dependencies / assumptions** — upstream timing, data guarantees, protocol assumptions, or hardware conditions relied upon
   - **Invariants** — what object/module state is preserved across all calls

3. **Express contracts in code** where the language supports it:
   - *C*: `DBC_REQUIRE(id, test)` / `DBC_ENSURE(id, test)` macros at function entry/exit (leave enabled in production firmware — they function as electronic fuses)
   - *C++*: `gsl::Expects()` / `gsl::Ensures()` from the C++ Core Guidelines support library; or C++26 `[[expects]]` / `[[ensures]]`
   - *Rust*: `#[requires(...)]` / `#[ensures(...)]` from the `contracts` crate; or type-state pattern for zero-cost compile-time contracts on hardware states

4. **Review for ambiguity** — for each field, ask: "could a caller and implementer interpret this differently?" Resolve ambiguities before writing implementation.

5. **Apply Interface Segregation** — split interfaces that span multiple unrelated responsibilities; each interface should represent one coherent behavioral contract.

6. **Identify verification and traceability implications** — what tests would falsify violations of this contract, and which stakeholder needs or requirements depend on this boundary?

7. **Identify compatibility and versioning implications** — if this contract changes, state whether existing callers can continue unchanged, whether a deprecation phase is needed, and what the likely SemVer impact is.

8. **State validation assumptions when relevant** — if the boundary exists to satisfy an operator, user, or integrator need, note what would have to be shown later to validate that the contract shape is fit for purpose.

## Contract inheritance rules (for subtyping)
- Preconditions can only be **weakened** in subclasses (accept at least what the parent accepted).
- Postconditions can only be **strengthened** in subclasses (guarantee at least what the parent guaranteed).
- Invariants can only be **strengthened**.
- Violating these rules breaks the Liskov Substitution Principle.

## Guardrails
- A contract specifies behavior at the boundary only — not internal implementation.
- Only include fields that callers actually depend on; do not over-specify.
- If timing constraints cannot be specified, mark them as "implementation-defined" rather than leaving them implicit.
- Do not stabilize a contract with known ambiguities — resolve them first.
- Do not change a public-facing contract without stating compatibility and migration implications.
- Do not leave interface ownership or external dependency assumptions implicit when they drive risk.
- In firmware assertion macros, use stable numeric IDs rather than `__LINE__` (line numbers shift; IDs are stable).
- Never assert on hardware-sourced data, sensor readings, or recoverable resource exhaustion — those are runtime conditions, not programmer bugs.

## When the contract is unclear
- **Callers disagree on semantics** — treat the most conservative interpretation as the contract; flag the divergence.
- **No existing callers** — define the contract from the use case, not the implementation.
- **Interface is too wide** — split into focused sub-interfaces; apply single responsibility.

## Done-when
- callers and implementers can agree on the same contract
- ambiguous behavior is removed
- verification expectations are clear

## Output
- contract (all ten fields per function)
- contract authority and dependency assumptions
- invariants
- failure modes
- requirement / stakeholder trace notes
- compatibility notes
- versioning or deprecation notes
- verification implications
