---
name: operation-cost-optimization
description: Optimize performance, endurance, churn, or footprint by measuring the real cost driver, assigning explicit weights where useful, and minimizing the score without changing required behavior. Use when flash erases/writes/reads, RAM or flash usage, heap traffic, copies/moves/constructions, I/O, locking, or similar costs dominate.
allowed-tools: Read, Grep, Glob, Bash
---

# Operation Cost Optimization

Optimize with evidence, not instinct. Count or measure the real cost driver — weighted for indirect costs, raw bytes for direct footprint — then reduce it without changing required behavior.

## Measurement order

Prefer the strongest signal that matches the claim:

1. direct bytes or resource usage for direct footprint claims
2. operation counts for indirect costs such as wear, churn, or hidden work
3. cycles, instructions, cache misses, or elapsed time as corroborating evidence

Do not start with elapsed time when a more direct cost signal is available.

## Typical fits

- flash-backed storage where erase/write frequency drives wear and latency
- RAM or flash footprint work where `.text`, `.rodata`, `.data`, `.bss`, stack, or heap pressure is the limiting budget
- C++ paths where constructions, copies, moves, allocations, or temporary objects are suspected to dominate
- queue, transport, logging, or serialization paths where the expensive work hides behind an interface
- firmware behavior that can be characterized in host simulation before target-hardware confirmation

## Tracking convention

Keep a durable optimization record on disk.

- Create or reuse the work packet under `docs/work/<work-id>/`.
- Use `docs/templates/optimization-scorecard-template.md`.
- Update the scorecard when the representative scenarios, baseline, current measurements, or tradeoffs change.
- Keep raw measurements visible alongside any weighted score.

## Process

1. **Pin down required behavior first** — read the brief, BDD scenarios, and current verification expectations.
   ```
   Read("docs/work/<work-id>/brief.md"), Glob("docs/work/<work-id>/evidence/**")
   ```
   Do not optimize an ambiguous requirement.

2. **Choose representative scenarios first** -- define the workloads, data sizes, failure cases, and steady-state or startup conditions that matter in real use.
   - The scenarios must be representative enough that the measured win is meaningful.
   - If the workload is synthetic, say what real behavior it is approximating.
   - If the workload is not representative, treat the result as exploratory rather than conclusive.

3. **Choose the cost model** -- name the thing being minimized, the representative scenarios to run, and the weight for each measured contributor when weighting is useful.

   Example indirect cost model:

   | Operation | Count source | Weight | Why |
   |---|---|---:|---|
   | flash erase | wrapped flash driver | 100 | wear + latency |
   | flash write | wrapped flash driver | 10 | wear + time |
   | flash read | wrapped flash driver | 1 | time only |
   | C++ copy | instrumented type / test double | 5 | churn + hidden work |
   | C++ move | instrumented type / test double | 2 | still non-free |
   | construction | instrumented type / allocator | 3 | allocation / setup |

   Weights may be heuristic or measured. State which they are.

   Example direct footprint model:

   | Contributor | Measurement source | Weight | Why |
   |---|---|---:|---|
   | `.data` bytes | linker map / `size` | 3 | consumes RAM and flash |
   | `.bss` bytes | linker map / `size` | 2 | consumes scarce RAM |
   | `.text` bytes | `bloaty` / `nm` | 1 | consumes flash |
   | worst-case stack bytes | stack watermark / `-fstack-usage` | 4 | overflow risk |

   For direct footprint work, raw bytes remain the primary signal. The weights help prioritize what to attack first when multiple sections matter.

4. **Create a measurement seam or attribution source** -- make the expensive contributor visible without changing semantics. Examples:
   - wrap flash operations in a counted adapter
   - inject a fake or probe object that records constructions, copies, moves, and destructions
   - count allocations through an allocator shim
   - collect linker map, `size`, `nm --size-sort`, `bloaty`, or stack-watermark outputs for direct RAM/flash attribution

5. **Baseline the current score** -- run the same representative scenarios and record:
   - per-operation counts or per-section bytes
   - weighted total score when a weighted model is being used
   - direct before/after measurements for RAM, flash, stack, or heap when those are the real target
   - any supporting timing, power, or endurance measurement that helps validate the proxy
   - enough repetitions or controls to distinguish signal from noise when timing is involved
   - the baseline in the optimization scorecard

6. **Optimize the dominant contributors first** -- prefer the smallest behavior-preserving change that removes high-weight operations.
   - batch or coalesce flash writes
   - avoid unnecessary erase cycles
   - reduce repeated reads with safe caching
   - shrink oversized static buffers or queues with evidence
   - deduplicate tables, strings, or template-heavy instantiations
   - move data to the cheapest valid storage class
   - tighten types or layouts when the interface contract still holds
   - reserve capacity
   - reuse objects
   - move instead of copy when ownership really transfers
   - remove temporary objects or repeated format conversions

7. **Use compiler and PMU evidence when relevant** -- before contorting source code, check whether the compiler or hardware counters already explain the cost.
   - For Clang/LLVM, use optimization remarks such as `-Rpass`, `-Rpass-missed`, `-Rpass-analysis`, or `-fsave-optimization-record` to see what transformed and what did not.
   - For GCC or Clang profile-guided optimization, only trust profile feedback when the training workload is representative.
   - For host-side measurement, `perf stat` or benchmark PMU counters can corroborate that a counted-cost win also reduced cycles, instructions, or cache pressure.

8. **Re-run behavior checks and the same scorecard** -- compare against the same scenarios after each change. Optimization does not count if the behavior, durability, freshness, or error handling regresses.

9. **Review tradeoffs explicitly** -- note any complexity, memory, latency-distribution, invalidation, or concurrency cost introduced by the optimization. A lower score is not a free pass for a fragile design.

10. **Keep only proven wins** -- remove speculative complexity. Leave behind lightweight counters only when they improve durable observability.

## Tooling patterns

- **Footprint attribution**
  - `size` for section totals
  - `nm --print-size --size-sort` for the largest symbols
  - `bloaty` for deep byte attribution and binary diffs
  - Zephyr `ram_report`, `rom_report`, `puncover`, and `pahole` when available
- **Runtime corroboration**
  - `perf stat` for hardware-counter-backed runs on Linux
  - Google Benchmark custom counters for domain-specific counts
  - Google Benchmark perf counters or memory-manager hooks when a benchmark harness already exists
- **Compiler guidance**
  - Clang/LLVM optimization remarks to explain missed vectorization, inlining, or loop transforms
  - PGO or sampling-based feedback only with representative workloads

## Variance control

When elapsed time or PMU counters matter:

- prefer fixed affinity, stable frequency settings, and repeated runs
- keep benchmark conditions stable enough that before/after comparisons are meaningful
- do not claim a win from a noisy single run
- if the environment is too noisy, fall back to stronger direct signals such as bytes or counted operations

## Guardrails

- Do not optimize before the required behavior is explicit.
- Do not optimize against toy inputs that fail to represent the real claim.
- Do not use a weighted score as a substitute for correctness.
- Do not count everything; choose the few operations most likely to dominate the real cost.
- Do not use a weighted score to hide the raw RAM or flash numbers; show both.
- Do not reduce the score by weakening durability, safety, freshness, or failure handling.
- Do not shrink buffers, tables, or stack margins without evidence that worst-case behavior still fits.
- Do not report a flash win while quietly moving the pressure into RAM, or the reverse.
- Do not trust PGO, perf, or benchmark numbers collected on unrepresentative workloads.
- Do not contort source code for a transformation the compiler is already doing.
- Do not hide risk in caches, pooling, or indirection without making invalidation, ownership, and lifetime rules explicit.
- Do not claim improvement without before/after measurements from the same representative scenarios.
- If the weighted proxy diverges from real outcomes, revise the model instead of forcing the conclusion.

## Done-when

- the expensive operations or footprint contributors and their weights are explicit
- the representative scenarios are explicit and believable
- the counting seam or attribution source is identified or implemented
- baseline and after-change counts or bytes are recorded
- the weighted score improved or the optimization idea was disproved
- required behavior is still demonstrated
- tradeoffs and residual risks are visible

## Output

- chosen cost model and weight rationale
- representative workload or scenario definition
- optimization scorecard created or updated
- instrumentation seam or attribution source
- representative scenarios
- before/after counts or bytes and weighted score where used
- corroborating compiler, PMU, or timing evidence when relevant
- behavior-preservation evidence
- tradeoffs, residual risks, and next candidates
