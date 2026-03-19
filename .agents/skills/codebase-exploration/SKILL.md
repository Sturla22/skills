---
name: codebase-exploration
description: Map the relevant files, entry points, boundaries, and invariants before changing code. Use when exploring an unfamiliar area, tracing ownership, mapping dependencies, finding test seams, or understanding module boundaries before making changes.
allowed-tools: Read, Grep, Glob, Bash
---

# Codebase Exploration

Understand the minimum relevant slice of the codebase before acting.

## Process

1. **Orient** — read top-level README, CLAUDE.md, and any manifest to establish language, build system, and major modules.
   ```
   Glob("**/{README*,CLAUDE.md,Cargo.toml,package.json,CMakeLists.txt,Makefile}")
   ```

2. **Read tests before source** — tests are the most reliable specification of intended behavior; scan integration tests first, then unit tests.
   ```
   Glob("**/{test,tests,spec}/**"), Grep("describe|#\[test\]|def test_|func Test")
   ```

3. **Find entry points** — locate `main`, top-level `init`, HTTP handlers, CLI commands, or the symbol named in the task. These are the canonical start nodes for traversal.
   ```
   Grep("<symbol>|fn main|int main|def main", type="<lang>")
   ```

4. **Map files and modules** — follow imports/includes one level deep; note ownership boundaries and high fan-in nodes (widely depended-upon = change-risky).

5. **Trace one representative flow end-to-end** — pick a single action or API call and follow it through all layers. Ask all three question types:
   - *What* does this component do?
   - *How* does it do it?
   - *Why* was it designed this way? (rationale — highest value)

6. **Spot beacons and deviations** — identify recurring idioms (retry loops, factory patterns, event dispatch). Deviations from the canonical form are where bugs live.

7. **Switch strategies when stuck** — alternate between top-down (read architecture, infer structure) and bottom-up (trace callstack, lift to abstraction). Experienced navigators switch opportunistically.

8. **Locate tests and seams** — find test files and interface/mock/stub boundaries near the change area.
   ```
   Grep("mock|stub|fake|double|spy")
   ```

9. **Externalize findings** — produce a running artifact (module map, hypothesis list, annotated call graph) before proceeding. Comprehension held only in memory degrades and cannot be shared.

## Guardrails
- Do not edit any file during exploration — read only.
- Stop tracing when you reach a stable external interface (stdlib, vendored lib, generated code).
- If the codebase is large, scope to the module named in the task rather than the whole repo.
- Do not infer ownership from file names alone — verify with `Grep` for usage.
- Do not mistake beacon recognition (pattern familiarity) for understanding — verify the pattern is used canonically.

## When exploration is inconclusive
- **Symbol not found** — try alternate spellings, macros, or generated code; note as unresolved if still missing.
- **Boundaries unclear** — treat the ambiguous area as in-scope and flag it in the output.
- **Too many entry points** — ask the user to narrow the scope before proceeding.
- **All top-down paths are opaque** — anchor on known platform/library call sites and work backward up the call stack (bottom-up lift via platform APIs).

## Done-when
- relevant files are identified
- boundaries and flow are summarized
- likely change points are named

## Output
- module map (top-level directories with one-line descriptions)
- entry points
- representative flow trace
- invariants and beacons
- test locations and seam boundaries
- open questions / unresolved areas
