---
name: validation-planning
description: Plan how to show that the work solves the real stakeholder need, not just that the implementation passes tests. Use when product behavior changes, multiple user or operator groups matter, measures of effectiveness or performance need to be defined, or verification alone would not show fitness for purpose.
allowed-tools: Read, Grep, Glob, Bash
---

# Validation Planning

Verification asks whether we built it right. Validation asks whether we built the right thing.

## Process

1. **Read the stakeholder-facing context** — start from the brief, requirements trace, scenarios, and any prior evidence.
   ```
   Read("docs/work/<work-id>/brief.md"), Read("docs/work/<work-id>/plan.md"), Glob("docs/work/<work-id>/evidence/**")
   ```

2. **State the stakeholder outcomes** — identify who must judge the result useful: user, operator, maintainer, integrator, downstream team, or release consumer.

3. **Define the validation question** — write what must be true for those stakeholders to say the result solved the problem.

4. **Choose success measures** — separate:
   - measures of effectiveness: did the outcome improve?
   - measures of performance: did the system meet the needed technical level?

5. **Define validation scenarios** — list the real usage or operational scenarios that matter. These may overlap with BDD scenarios but should be framed in terms of stakeholder fit, not just implementation behavior.

6. **Plan the evidence source** — decide whether validation will use demos, pilot usage, operator walkthroughs, benchmark thresholds, field logs, acceptance sessions, or explicit sign-off by a named stakeholder group.

7. **Record what remains outside validation** — be honest about what this plan will not prove, especially if only a lightweight validation approach is practical.

Use `docs/templates/validation-template.md`.

## Guardrails
- Do not substitute passing automated tests for validation.
- Do not create a heavyweight validation ritual for tiny internal changes that have no stakeholder-fit question.
- Do not leave measures of effectiveness implicit when the work changes user-facing value.
- Do not claim validation evidence you do not yet have.

## When validation is weak
- **No clear stakeholder exists** — validation is probably not the right focus; stay at verification.
- **The outcome is qualitative** — use a structured walkthrough, pilot, or explicit acceptance conversation rather than forcing fake metrics.
- **Measures are too vague** — rewrite them so someone could tell pass from fail.
- **Validation depends on future release usage** — document the deferred evidence and the trigger for collecting it.

## Done-when
- stakeholder outcomes are explicit
- success measures are explicit
- validation scenarios and evidence sources are explicit
- limits of the validation plan are stated honestly

## Output
- stakeholders and outcomes
- validation question
- measures of effectiveness / performance
- validation scenarios
- evidence plan
- validation gaps or deferred evidence
