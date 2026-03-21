---
name: trade-study-and-decision-analysis
description: Compare viable options against explicit criteria and choose a justified direction. Use when multiple architectures, interfaces, rollout shapes, or implementation concepts are plausible and the team needs a clear, evidence-based decision instead of intuition-only selection.
allowed-tools: Read, Grep, Glob, Bash
---

# Trade Study and Decision Analysis

Choose deliberately when more than one credible path exists.

## Process

1. **State the decision to be made** — one sentence describing the actual choice, not a vague design area.

2. **Read the governing context** — brief, plan, requirements, constraints, and existing architecture notes.
   ```
   Read("docs/work/<work-id>/brief.md"), Read("docs/work/<work-id>/plan.md"), Glob("docs/work/<work-id>/evidence/**"), Glob("docs/**/*.md")
   ```

3. **List real options** — include at least two viable alternatives at the same abstraction level. If one option is obviously impossible, it is not a real option and should not be included to pad the analysis.

4. **Define decision criteria** — choose criteria that matter for this decision, such as:
   - requirement fit
   - interface stability
   - verification cost
   - validation risk
   - performance / resource impact
   - migration cost
   - rollout reversibility
   - operational or safety risk

5. **Assess options explicitly** — capture evidence, assumptions, and tradeoffs for each option. Use weighting only when it genuinely clarifies the choice; avoid fake precision.

6. **Test sensitivity** — ask what assumption or criterion would have to change for a different option to become preferable. This catches brittle recommendations.

7. **Recommend one option and state why** — include the consequences, migration implications, and what must be true for the recommendation to remain valid.

Use `docs/templates/trade-study-template.md`.

## Guardrails
- Do not compare options at different abstraction levels.
- Do not use dummy alternatives to make the preferred option look inevitable.
- Do not hide decisive assumptions.
- Do not pretend scoring is objective if the inputs are uncertain.
- Do not skip reversibility and migration impact on system-level choices.

## When trade studies stall
- **Options are fuzzy** — tighten the decision statement first.
- **Criteria are too many** — keep only the criteria that would change the recommendation.
- **Evidence is weak** — turn the uncertainty into a spike or experiment rather than bluffing certainty.
- **Two options are nearly tied** — prefer the more reversible path unless a stronger requirement says otherwise.

## Done-when
- the decision is explicit
- viable options were compared fairly
- criteria and assumptions are visible
- one recommendation is justified
- consequences and migration impact are stated

## Output
- decision statement
- options considered
- criteria used
- evidence and assumptions
- recommendation
- consequences and sensitivity notes
