---
name: workflow-evolution
description: Improve the roles-and-skills system from evidence in durable work artifacts. Use when repeated friction, unclear role boundaries, stale prompts, missing templates, or a possible new skill or role needs a disciplined workflow change.
allowed-tools: Read, Grep, Glob, Bash
---

# Workflow Evolution

Improve the process based on evidence, not vibes.

## Process

1. **Collect durable evidence** — read the relevant work packets, handoffs, prompts, role files, skills, and docs. Favor repeated patterns over isolated complaints.
   ```
   Glob("docs/work/**"), Read("AGENTS.md"), Glob(".agents/agents/*.toml"), Glob(".agents/skills/*/SKILL.md"), Read("templates/reusable-prompts.md")
   ```

2. **State the recurring problem** — summarize the friction operationally:
   - what keeps going wrong or staying unclear
   - where it shows up
   - who is affected
   - what cost it creates

3. **Choose the smallest intervention** — prefer the lightest fix that can plausibly solve the problem:
   - prompt tweak
   - template change
   - Claude-native runtime change such as settings, rules, hooks, output styles, or `.mcp.json`
   - docs/playbook update
   - skill update or new skill
   - role update or new role

4. **Choose one small mutable surface** — change one prompt, one template, one skill, one role, or one tightly-related doc slice at a time whenever possible. If several surfaces must change together, explain why attribution will still be clear.

5. **Define the experiment window and signals** — record:
   - the bounded change being tested
   - the evaluation window, such as the next `3` work packets or one milestone
   - the success signals
   - the failure signals or revert triggers

Use `templates/workflow-experiment-template.md` and store the record under `docs/workflow-experiments/`.

6. **Apply the escalation ladder explicitly** — write down why lower-cost fixes are insufficient before creating a new role. The default order is:
   - prompt or template
   - tool-native runtime file when the problem is Claude-specific
   - skill
   - role

7. **Define sharp boundaries** — if a skill or role is needed, make its trigger, boundary, inputs, outputs, and non-goals explicit. Avoid overlap with existing roles unless the distinction is concrete and useful.

8. **Treat workflow changes as contract changes** — state SemVer impact, update `CHANGELOG.md`, and note migration or onboarding consequences when downstream users must adapt.

9. **Close the loop explicitly** — after the evaluation window, decide whether to keep, revise, or revert the change. A workflow experiment is incomplete without that decision.

## Guardrails
- Do not create a new role for a one-off pain point.
- Do not use workflow work to smuggle in unrelated product decisions.
- Do not optimize the process without evidence from real work artifacts.
- Do not add overlapping responsibilities unless the separation of concerns is explicit.
- Do not let "monitoring" become silent interference in active delivery work; default to reviewing durable artifacts and explicit checkpoints.
- Do not create a new skill if a template or prompt change is enough.
- Do not mutate several workflow surfaces at once if that would make the result impossible to attribute.
- Do not leave workflow experiments open-ended with no evaluation window or closure decision.

## When workflow change stalls
- **The evidence is weak** — collect more examples from work packets before changing the model.
- **Two interventions seem plausible** — choose the more reversible one first.
- **A new role seems tempting** — try to prove a skill or template is insufficient.
- **The change is broad** — land the smallest slice that can be tested in real usage.

## Done-when
- the recurring friction is stated clearly
- the chosen intervention is the smallest plausible fix
- boundaries and non-goals are explicit
- the experiment window and signals are explicit
- SemVer / changelog impact is handled
- success signals are defined
- keep / revise / revert is recorded

## Output
- recurring pattern
- evidence used
- chosen intervention type
- boundaries and non-goals
- experiment window and signals
- repo changes
- SemVer / changelog impact
- success signals
- keep / revise / revert decision
