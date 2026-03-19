---
name: bdd
description: Discover and formulate behavior through concrete examples before or alongside implementation. Use when shaping acceptance criteria, turning a brief into rules and examples, mapping scenarios onto the test pyramid, or aligning product behavior before TDD.
allowed-tools: Read, Grep, Glob, Bash
---

# BDD

Discover rules through concrete examples, formulate them as shared scenarios, then map each to the cheapest trustworthy test level. BDD defines the behavior and shared language; TDD drives the implementation.

## Preferred strategy

- Start with conversation about concrete examples, not syntax.
- Capture business rules, examples, open questions, and deferred slices before automating anything.
- Express product behavior in scenario form once the examples are concrete enough to check shared understanding.
- Prefer Given/When/Then style thinking, but do not force ceremony when a short behavioral statement is clearer.
- Use the language of the user, operator, caller, or domain expert, not internal implementation names.
- Prefer one rule per scenario, and group related scenarios under a rule when helpful.
- Map each scenario onto the test pyramid at the lowest sensible level.
- Prefer host simulation for executable behavior scenarios before target-hardware checks when hardware is not essential to the claim.
- Prefer connecting scenarios below the UI when the claim is really about business or firmware behavior rather than screen flow.

## Process

1. **Read the brief and current behavior** — understand the desired outcome, current constraints, and where behavior is already documented.
   ```
   Read("<brief-or-task>"), Glob("**/{README*,docs/**,test,tests,spec}/**")
   ```

2. **Discover rules through concrete examples** — ask for or construct realistic examples before writing polished scenarios.
   - Capture:
     - business rules
     - concrete examples and edge cases
     - open questions
     - out-of-scope or deferred cases
   - Prefer real nouns, amounts, identifiers, dates, states, and failure conditions over placeholders when that improves clarity.
   - If examples reveal unresolved policy decisions, stop pretending the behavior is settled and hand the ambiguity back up.

3. **Formulate behavior scenarios** — turn the stable examples into observable scenarios.
   - Prefer user-visible or caller-visible outcomes.
   - Focus on intent, not implementation.
   - Prefer one rule per scenario.
   - Keep scenarios short and memorable.
   - Use `Rule` grouping when multiple scenarios illustrate the same business rule.
   - Keep `Background` short if used at all; if it starts carrying important behavior, make that behavior explicit in the scenario instead.
   - Example:
     ```text
     Given the sensor input is stale
     When the controller computes the next output
     Then it rejects the stale value and reports a recoverable fault
     ```

4. **Separate policy from mechanism** — make sure each scenario describes what must happen, not which function, class, screen widget, or internal variable must change.

5. **Choose the test level for each scenario** — assign each behavior to the lowest sensible level:
   - unit for pure decision logic
   - integration for module boundaries and contracts
   - end-to-end or HIL for full workflows or hardware-dependent claims

6. **Prefer simulation-first execution** — when hardware is not essential, run the scenario in a deterministic host harness before using target hardware. If the scenario is currently only testable through the UI or hardware, ask whether the architecture should expose a cheaper seam.

7. **Hand scenarios to TDD or verification** — once the behavior is explicit, drive implementation with `tdd` and demonstrate the claim with `verification`.

## Guardrails

- Do not treat BDD as "write Gherkin after the code exists."
- Do not confuse discovery with typing a feature file in real time.
- Do not write scenarios in terms of private state or internal implementation details.
- Do not write UI-driven procedural scripts unless the UI flow itself is the required behavior.
- Do not explode one behavior into dozens of cosmetic variants; keep the scenario set minimal but discriminating.
- Do not pack multiple rules into one long scenario.
- Do not force Gherkin formatting when a concise behavioral statement is clearer.
- Do not bury important behavior in a long `Background`, giant table, or example outline with incidental detail.
- Do not automate every example discussed; automate the smallest set that nails the rule and edge cases.
- If a domain expert would not recognize the wording, the shared language is drifting.
- If a scenario can only be checked on hardware, say so explicitly.
- If the acceptance criteria cannot be written as observable behavior, the brief is still too vague.

## Done-when

- the key business rules and concrete examples are explicit
- the intended behavior is expressed in observable scenarios
- open questions or deferred slices are visible
- each scenario has a sensible test level
- simulation-first opportunities are named

## Output

- business rules
- concrete examples and edge cases
- open questions or deferred slices
- behavior scenarios
- edge cases and failure behaviors
- test-level mapping
- hardware-only gaps
