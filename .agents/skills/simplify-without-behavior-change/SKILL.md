---
name: simplify-without-behavior-change
description: Remove accidental complexity without changing externally visible behavior. Use when code feels overengineered, wrappers add little value, flags or state paths are tangled, obsolete options or branches remain, or before a refactor to reduce noise.
argument-hint: "[file-or-module-to-simplify]"
allowed-tools: Read, Grep, Glob, Bash
---

# Simplify Without Behavior Change

Eliminate accidental complexity. Essential complexity (required by the problem) stays; accidental complexity (required only by past implementation choices) goes.

## Principles (in priority order — Kent Beck's Rules of Simple Design)
1. **Passes the tests** — behavior must be preserved. Non-negotiable.
2. **Reveals intention** — code communicates its purpose clearly.
3. **No duplication** — everything said once and only once.
4. **Fewest elements** — delete anything not needed by rules 1–3. The burden of proof is on the element's existence, not its removal.

## Complexity smell taxonomy — target these first

| Smell | Signal |
|---|---|
| **Speculative Generality** | Hooks, abstract classes, or parameters added for requirements that never arrived (YAGNI violation) |
| **Dead Code** | Variables, methods, or branches unreachable by any execution path |
| **Lazy Element** | Class or method that doesn't justify its existence — too thin, too delegating |
| **Middle Man** | Class that does nothing but delegate — pure indirection tax with no abstraction |
| **Duplicate Code** | Same logic in more than one place |
| **Control Flag** | Boolean variable controlling loop/conditional flow that could be a `break`, `return`, or `continue` |
| **Magic Literal** | Bare constant with no named meaning |

## Process

1. **Read the target** — understand what behavior must be preserved and where the complexity lives.
   ```
   Read("<target-file>"), Grep("<key-symbol>")
   ```

2. **State the behavior that must remain** — write it down before touching anything.

3. **Distinguish essential from accidental** — for each complex element, ask:
   - What driver does this element serve — user scenario, risk, epistemic uncertainty, design intent communication, or external obligation? If none, it is accidental.
   - Is this required by the problem domain, or by our solution?
   - What would happen if we removed it? Would a user-visible requirement break?
   - Is this here because of a real past failure, or a hypothetical future one?
   - Does this complexity have a proportionate benefit (performance, correctness, safety)?

4. **Add characterization tests if coverage is weak** — lock behavior before simplifying.

5. **Apply one concrete simplification move at a time:**
   - **Inline Function** — when the body is more obvious than the name, or it's a thin delegate.
   - **Remove Middle Man** — callers can call the delegate directly.
   - **Remove Control Flag** — replace with structured exits.
   - **Delete Dead Code** — confirmed unreachable by static analysis + coverage; don't comment out.
   - **Collapse Hierarchy** — when a subclass adds nothing to a parent.
   - **Remove Flag Argument** — split a function with a boolean behavior-switch into two named functions.

6. **Re-run tests after each simplification** — if any test fails, revert that step.

## Guardrails
- Do not simplify and add features in the same step.
- Do not remove a branch or option without confirming it is genuinely unreachable or unused.
- If simplification uncovers a real bug, stop and create a separate fix task — do not fix inline.
- Keep each change small enough to revert independently.
- YAGNI applies only to capabilities for presumed future requirements that haven't arrived — not to effort spent making code easy to change (tests, good naming, refactoring).

## When simplification is blocked
- **No tests cover the area** — add characterization tests first (see `tdd`).
- **Complexity is load-bearing** — document why and leave it; note it in the output as essential.
- **Behavior is unclear** — use `codebase-exploration` to understand it before simplifying.

## Done-when
- same visible behavior
- fewer moving parts
- fewer special cases
- easier to explain

## Output
- preserved behavior (stated)
- accidental complexity found (with smell name)
- simplifications made (one line each)
- items removed
- verification summary
