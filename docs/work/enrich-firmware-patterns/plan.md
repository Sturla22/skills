# Plan: enrich-firmware-patterns

**Work ID:** enrich-firmware-patterns
**Date:** 2026-03-20
**Owner:** planner
**Status:** Ready for developer handoff — one product-owner clarification needed (see section 13)

---

## 1. Operational problem statement

The firmware skills in `.agents/skills/*/SKILL.md` carry thin or C-biased examples. Practitioners reading them get no guidance on the 14 C++ embedded design patterns documented in `evidence/research-cpp-embedded-patterns.md`. The work is done when every researched pattern is represented by at least one targeted addition in the most appropriate existing skill, and when `python3 scripts/sync_agent_layouts.py` has propagated each update to all downstream layouts.

---

## 2. Delivery class and TDD expectation

Non-productized tool update (repo skill enrichment). TDD is not required.

Replacement verification: structural grep check confirming key terms from each pattern appear in the target skill file, combined with a diff confirming no prior content was removed. See section 8.

---

## 3. Stakeholders and system context

| Stakeholder | Interest |
|---|---|
| Firmware engineers using this repo | Richer C++ guidance in the skills they already reach for |
| Product-owner | Approved research; expects focused enrichment, not bloat |
| Future planners and reviewers | Canonical skill files remain focused and not aggregated |

External interface: `scripts/sync_agent_layouts.py` propagates `.agents/skills/*/SKILL.md` to `.claude/skills/`, `.codex/`, and `.github/` layouts. Canonical edits must land in `.agents/skills/*/SKILL.md` only.

---

## 4. Contract surfaces touched and SemVer impact

Files that will be modified:

- `.agents/skills/hardware-abstraction/SKILL.md`
- `.agents/skills/simulation-harness-first/SKILL.md`
- `.agents/skills/tdd/SKILL.md`
- `.agents/skills/interface-contract-design/SKILL.md`
- `.agents/skills/resource-budget-review/SKILL.md`

SemVer impact: **MINOR** — adds guidance and examples; no backward-incompatible changes to existing skill contracts. `CHANGELOG.md` should record this under `Added`.

No new skill files are proposed (see section 6 for rationale).

---

## 5. Pattern-to-skill mapping

All 14 researched patterns (9 seed + 5 surfaced extras) are mapped. Mapping principle: place each pattern in the skill where a practitioner would look for it.

| # | Pattern | Target skill | Rationale |
|---|---|---|---|
| 1.1 | Active Object | `simulation-harness-first` | Primary concern is faking the AO queue and task context in host tests. Sizing note also in `resource-budget-review`. |
| 1.2 | Ring buffer / SPSC | `tdd` | SPSC correctness properties are driven by tests; ISR-to-task ordering is a behavioral claim. Cortex-M0 atomic gap is a guardrail. |
| 1.3 | Command queue / message-passing | `simulation-harness-first` | Decouple queue from RTOS task context in simulation. Overflow contract cross-references `interface-contract-design`. |
| 2.1 | Policy-based design | `hardware-abstraction` | Policy types are the compile-time HAL alternative; practitioners read this skill when deciding how to abstract hardware. |
| 2.2 | CRTP | `hardware-abstraction` | CRTP for zero-cost driver interfaces belongs next to policy-based design; both are compile-time abstraction options. |
| 3.1 | ETL library overview | `simulation-harness-first` | `etl::queue` and `etl::circular_buffer` are canonical bounded fake containers for host simulation. MISRA gap note lives here. |
| 3.1a | ETL type erasure (`etl::imessage`, `etl::ifsm_state`) | `interface-contract-design` | Non-template base interfaces are an interface-design decision, not a simulation choice. |
| 4.1 | Placement new for MMIO | `hardware-abstraction` | Typed MMIO register access extends the existing "opaque handles" guidance. `volatile`+barrier gap note lives here. |
| 4.E | RAII for peripheral ownership | `hardware-abstraction` | Peripheral lifecycle RAII is the companion to placement new; same skill section covers lifecycle management. |
| 5.1 (flat/table) | State machine — flat/table-driven | `tdd` | Table-driven FSMs have a direct TDD idiom: one test per transition row drives the table. |
| 5.1 (HSM) | State machine — hierarchical | `simulation-harness-first` | Faking RTOS event dispatch for HSM testing is the primary simulation challenge. |
| 5.1 (variant) | State machine — `std::variant`-based | `tdd` | `std::variant` FSMs are host-testable; exhaustive-handling enforcement is a compile-time TDD benefit. Toolchain gap note lives here. |
| 6.1 | Observer / event bus | `interface-contract-design` | Registration order, capacity contract, and ISR-safe notification are interface contract questions. |
| A | Delegate / callback wrapper (`etl::delegate`) | `interface-contract-design` | Heap-free callable ownership and lifetime belong in the interface ownership / resource contract section. |
| B | Memory pool | `resource-budget-review` | Pool sizing and acquire/release overhead are resource-review checklist items. |
| C | Double buffer / ping-pong buffer | `resource-budget-review` | 2x RAM cost and swap synchronization overhead are resource-review checklist items. |

---

## 6. New skill justification: no new skills

- Active Object splits cleanly across `simulation-harness-first` and `resource-budget-review`. A standalone skill would be thin or duplicate two existing skills.
- State machine variants split cleanly: flat/variant into `tdd`, HSM into `simulation-harness-first`. Aggregating all three would work against the "keep skills focused" constraint.
- ETL as a library is a tooling reference used inline where relevant; a standalone `etl` skill would not match how practitioners search for guidance.

Decision: enrich existing skills only.

---

## 7. Parallel lanes, write surfaces, and isolation plan

### Serial step 0 — verify sync script baseline

Owner: developer
Write surface: none
Action: `python3 scripts/sync_agent_layouts.py` on unmodified tree; confirm exit 0.
Blocker: if script fails, all lanes are blocked; escalate to product-owner.

---

### Lane A — hardware-abstraction enrichment

Worktree: `git worktree add /tmp/wt-enrich-hw-abstraction -b enrich/hw-abstraction`
Write surface: `.agents/skills/hardware-abstraction/SKILL.md` only

Patterns:
- **Policy-based design (2.1):** Template-parameter policy as compile-time HAL alternative alongside existing `IUart` virtual example. Note Empty Base Class Optimization for stateless policies.
- **CRTP (2.2):** Zero-cost driver interface via CRTP. Include private-constructor + friend guard. Note C++23 deducing-`this` unavailable on C++11/14/17 targets.
- **Placement new for MMIO (4.1):** Typed MMIO accessor via placement new in the "opaque handles" step. Note `volatile` propagation; add `std::launder` C++17 note: "`std::launder` (C++17) is required for strict conformance; on C++11/14 this is technically UB but compilers do not miscompile it in practice — note in safety-critical contexts."
- **RAII for peripheral ownership (4.E):** SPI bus lock, GPIO enable/disable, power-rail guards as RAII examples in step 5.

Required guardrail addition:
> "On multi-core or DMA-capable SoCs, `volatile` alone does not guarantee memory ordering; add explicit memory barriers (`DMB`/`DSB` on ARM, or `std::atomic_thread_fence`) for shared MMIO regions accessed by DMA or a second core."

Final step: `python3 scripts/sync_agent_layouts.py`
Done-when: `policy`, `CRTP`, `placement new`, `volatile`, `RAII` findable by grep; script exits 0; zero deletions.

---

### Lane B — simulation-harness-first enrichment

Worktree: `git worktree add /tmp/wt-enrich-sim-harness -b enrich/sim-harness`
Write surface: `.agents/skills/simulation-harness-first/SKILL.md` only

Patterns:
- **Active Object (1.1):** In "Implement test doubles": fake an AO's private queue as a synchronous call in host tests (caller posts; fake drains immediately in the same thread). The real RTOS task is replaced by the test runner.
- **Command queue / message-passing (1.3):** Concrete fake-queue example showing bounded capacity enforcement; overflow policy must be explicit in the double.
- **ETL (3.1):** In "Tooling options": `etl::queue<T,N>` and `etl::circular_buffer<T,N>` as compile-time-fixed containers eliminating heap allocation in test doubles. Add required MISRA note.
- **HSM (5.1):** Drive HSM event dispatch from a synchronous test loop; RTC step timing must be measured on the actual target before committing to deep hierarchies.

Required wording:
- ETL MISRA: "ETL is not formally MISRA-certified; audit against your applicable MISRA C++ subset before adopting in safety-critical contexts."
- AO sizing: "Queue depth and task stack depth for Active Objects are workload-dependent; no platform-agnostic rule exists — size by workload analysis on the deployment target."

Final step: `python3 scripts/sync_agent_layouts.py`
Done-when: `Active Object` (case-insensitive), `etl::` or `ETL`, `MISRA`, `HSM` or `hierarchical` findable by grep; script exits 0; zero deletions.

---

### Lane C — tdd enrichment

Worktree: `git worktree add /tmp/wt-enrich-tdd -b enrich/tdd`
Write surface: `.agents/skills/tdd/SKILL.md` only

Patterns (all to the existing "Embedded-specific" section or adjacent subsection):
- **Ring buffer / SPSC (1.2):** Test producer/consumer separation; assert full/empty detection boundary conditions. Add required guardrail.
- **Table-driven FSM (5.1 flat):** One test per row of the transition table; missing row = test failure; table consistency must be maintained alongside tests.
- **`std::variant`-based FSM (5.1 variant):** `std::visit` with overload pattern makes exhaustive event handling a compile-time check; test that unhandled events fail to compile. Add toolchain note.

Required guardrail:
> "Lock-free SPSC ring buffer correctness requires `std::atomic` with `memory_order_acquire`/`memory_order_release`; `volatile` alone is insufficient. On Cortex-M0/M0+ without `LDREX`/`STREX`, disable interrupts instead of relying on lock-free atomics."

Required toolchain note:
> "`std::variant`-based FSMs require C++17; confirm toolchain support and `-fno-exceptions` configuration before using on constrained targets."

Final step: `python3 scripts/sync_agent_layouts.py`
Done-when: `ring buffer` or `circular buffer`, `SPSC` or `spsc`, `table-driven`, `std::variant` findable by grep; script exits 0; zero deletions.

---

### Lane E — resource-budget-review enrichment (parallel with A/B/C)

Worktree: `git worktree add /tmp/wt-enrich-resource -b enrich/resource`
Write surface: `.agents/skills/resource-budget-review/SKILL.md` only

Patterns (additions to existing "Review checklist"):
- **Memory pool (B):** Fixed-block allocator acquire/release overhead; block size must cover worst-case object; check `etl::pool` capacity against worst-case concurrent acquisition count.
- **Double buffer / ping-pong (C):** Double-buffer RAM cost is 2x; swap synchronization must be accounted for; DMA alignment requirement applies to both buffers.
- **Active Object queue/stack sizing (1.1 cross-ref):** AO queue depth and task stack depth are first-class resource review items; cross-reference `simulation-harness-first` for workload-sizing guidance.

Final step: `python3 scripts/sync_agent_layouts.py`
Done-when: `memory pool` or `etl::pool`, `double buffer` or `ping-pong`, `queue depth` or `stack depth` findable by grep; script exits 0; zero deletions.

---

### Lane D — interface-contract-design enrichment (serial, after A/B/C/E merge)

Lane D is placed last because it cross-references ETL and observer concepts introduced in Lanes A and B; reviewing the merged state before editing reduces inconsistency risk.

Worktree: `git worktree add /tmp/wt-enrich-icd -b enrich/icd` (if needed)
Write surface: `.agents/skills/interface-contract-design/SKILL.md` only

Patterns:
- **ETL type erasure (3.1a):** In "Apply Interface Segregation": `etl::imessage`, `etl::ifsm_state`, `etl::icircular_buffer` provide lightweight type-erasure seams for heterogeneous storage without RTTI.
- **Observer / event bus (6.1):** In "Concurrency / reentrancy" contract field: notification order is deterministic (registration order); ISR-safe notification requires every observer's `notification()` to be ISR-safe; prefer posting to a queue and notifying from task context. Add ETL `etl::observer_list_full` as a contract invariant. Note observers cannot be removed during traversal.
- **Delegate / callback wrapper (A):** In "Ownership" contract field: `etl::delegate` is a heap-free callable; captured object's lifetime must not exceed the delegate's owner's lifetime.

Required wording:
> "If `notify_observers()` can be called from ISR context, every observer's `notification()` must be ISR-safe — prefer posting to a queue and notifying from task context instead."

Final step: `python3 scripts/sync_agent_layouts.py`
Done-when: `observer`, `etl::delegate` or `delegate`, `imessage` or `type erasure` findable by grep; script exits 0; zero deletions.

---

### Merge and integration checkpoint

After all five lanes complete:
1. Merge feature branches into `main` (one commit per lane, Conventional Commit style).
2. `python3 scripts/sync_agent_layouts.py` on merged tree; confirm exit 0.
3. Run structural verification check (section 8).
4. Spot-check one propagated file in `.claude/skills/` for propagation.
5. Update `docs/work/enrich-firmware-patterns/status.md` to completed.
6. Update `CHANGELOG.md` under `Unreleased → Added`.

---

## 8. Verification expectations

### Structural verification checklist

Run after all lanes are merged and sync script has passed.

| Skill file | Required grep terms | Absence = failure |
|---|---|---|
| `hardware-abstraction/SKILL.md` | `policy`, `CRTP`, `placement new`, `volatile`, `RAII` | yes |
| `simulation-harness-first/SKILL.md` | `Active Object` (case-insensitive), `etl::` or `ETL`, `MISRA`, `HSM` or `hierarchical` | yes |
| `tdd/SKILL.md` | `ring buffer` or `circular buffer`, `SPSC` or `spsc`, `table-driven`, `std::variant` | yes |
| `interface-contract-design/SKILL.md` | `observer`, `delegate`, `imessage` or `type erasure` | yes |
| `resource-budget-review/SKILL.md` | `memory pool` or `etl::pool`, `double buffer` or `ping-pong`, `queue depth` or `stack depth` | yes |

Additional:
- Diff each target skill against pre-change baseline: zero lines deleted.
- `python3 scripts/sync_agent_layouts.py` exits 0 on final merged tree.
- Spot-check one `.claude/skills/` file for propagation.

---

## 9. Research gap handling

| Gap | Where it lands | Required wording |
|---|---|---|
| Lock-free ring buffer ISA caveat (Cortex-M0) | `tdd/SKILL.md` guardrail | Lane C required guardrail |
| ETL MISRA non-certification | `simulation-harness-first/SKILL.md` | Lane B required wording |
| `std::variant` toolchain caveat | `tdd/SKILL.md` | Lane C required toolchain note |
| `volatile` alone insufficient for MMIO on multi-core/DMA | `hardware-abstraction/SKILL.md` guardrail | Lane A required guardrail |
| Active Object queue/stack sizing workload-dependency | `simulation-harness-first` + `resource-budget-review` | Lane B and E required wording |
| `std::launder` C++11/14 gray area | `hardware-abstraction/SKILL.md` placement new note | Lane A `std::launder` note |

---

## 10. Ordered execution summary

```
[serial]   Step 0: verify sync script runs clean on current tree
           |
           +--- [parallel] Lane A: hardware-abstraction
           |               patterns: policy-based design, CRTP, placement new, RAII
           |               worktree: /tmp/wt-enrich-hw-abstraction
           |
           +--- [parallel] Lane B: simulation-harness-first
           |               patterns: Active Object, command queue, ETL, HSM
           |               worktree: /tmp/wt-enrich-sim-harness
           |
           +--- [parallel] Lane C: tdd
           |               patterns: ring buffer/SPSC, table-driven FSM, std::variant FSM
           |               worktree: /tmp/wt-enrich-tdd
           |
           +--- [parallel] Lane E: resource-budget-review
                           patterns: memory pool, double buffer, AO sizing
                           worktree: /tmp/wt-enrich-resource
           |
[serial]   Merge A, B, C, E → integration checkpoint (sync + spot-check)
           |
[serial]   Lane D: interface-contract-design
           |       patterns: ETL type erasure, observer/event bus, delegate
           |
[serial]   Final sync + structural verification
           |
[serial]   Update status.md, CHANGELOG.md
```

---

## 11. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Sync script fails on merged tree | Low | Run sync at end of each lane before merge |
| Developer deletes existing content | Low | Structural diff check (zero deletions) is a hard gate |
| Lane D wording inconsistent with ETL references from A/B | Low | Lane D placed last; developer reviews merged state before editing |
| Toolchain notes inaccurate | Low | Required wording specified in plan; verifier checks exact terms |
| Lane write surface overlap | None | Each lane has exactly one target file; enforced by worktree isolation |

---

## 12. Conditions that require return to product-owner

- Sync script fails with a non-trivial error
- Any developer proposes removing existing skill content (zero-deletion gate breach)
- Q1 answer identifies a pattern warranting a new skill file (scope change)
- A researched pattern conflicts with existing guidance in a skill — flag before inserting

---

## 13. Items requiring product-owner clarification before work starts

**Q1 — firmware-migration enrichment scope:** The research does not surface any pattern with a strong natural home in `firmware-migration/SKILL.md`. The closest candidate (RAII peripheral ownership) maps more cleanly to `hardware-abstraction`. Should `firmware-migration` receive any enrichment, or is the mapping in section 5 complete?

If the answer is "no enrichment needed," the plan proceeds as written. All lanes A–E are unblocked. This is the only open question.
