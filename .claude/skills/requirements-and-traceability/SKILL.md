---
name: requirements-and-traceability
description: Capture stakeholder needs, explicit requirements, derived requirements, and their links to design, verification, and validation evidence. Use when expected behavior is unclear, requirements may drift across handoffs, multiple stakeholders matter, or traceability is needed for safety, release, or systems work.
allowed-tools: Read, Grep, Glob, Bash
---

# Requirements and Traceability

Keep system intent connected to the work instead of letting it dissolve into scattered notes.

## Process

1. **Read the durable context** — use the brief, plan, status, and evidence as the working truth.
   ```
   Read("docs/work/<work-id>/brief.md"), Read("docs/work/<work-id>/plan.md"), Read("docs/work/<work-id>/status.md"), Glob("docs/work/<work-id>/evidence/**")
   ```

2. **Identify the source statements** — separate:
   - stakeholder needs
   - explicit requirements
   - derived requirements
   - constraints
   - assumptions that are not yet requirements

3. **Write each requirement so it can be checked** — make it specific enough that a reviewer could tell whether it is met. If a requirement is ambiguous, push it back for clarification instead of preserving the ambiguity in polished prose.

4. **Assign stable IDs and capture source** — use durable identifiers and record where the need or requirement came from: requester statement, brief, standard, defect report, interface contract, or architectural constraint.

5. **Trace each requirement forward** — link it to:
   - acceptance criteria or BDD scenario
   - design element or interface
   - planned verification method
   - planned validation evidence when relevant

6. **Trace each requirement backward when needed** — confirm that derived requirements and technical constraints still point back to a real stakeholder need, system goal, or external constraint.

7. **Capture impact analysis when things change** — when a requirement, design criterion, interface, or major assumption changes, state what downstream design elements, tests, validation evidence, docs, or teams are affected.

8. **Keep the trace lightweight and alive** — update the trace record when requirements split, merge, get superseded, or become invalid. A small accurate trace is better than a large stale one.

Use `templates/requirements-traceability-template.md`.

## Guardrails
- Do not turn every observation into a requirement.
- Do not leave stakeholder needs implicit when they drive tradeoffs or validation.
- Do not confuse assumptions with approved requirements.
- Do not create traceability theater; keep only links that help decisions, verification, validation, or downstream adaptation.
- Do not accept unverifiable requirements as "good enough."
- Do not make a requirement or interface change without thinking through downstream impact.

## When traceability is weak
- **Expected behavior is disputed** — write the stakeholder need and the acceptance behavior side by side.
- **A derived requirement has no clear source** — challenge it before cementing it into design.
- **The trace matrix is exploding** — split by subsystem or by delivery slice; keep each trace set scoped to the work packet.
- **Verification exists but rationale is missing** — add the requirement-to-check link before claiming confidence.

## Done-when
- stakeholder needs and requirements are explicit
- derived requirements have a visible source
- key requirements are linked to design, verification, and validation
- downstream impact is visible when important things changed
- ambiguous or orphaned requirements are called out

## Output
- stakeholder needs
- explicit and derived requirements
- trace links
- impact analysis
- ambiguities or orphaned requirements
- updates to the durable trace record

## Relation to scenario traceability

For lightweight need → test linkage without full requirements formalism, use
the `scenario-traceability` skill: plain-English `SC-NNN` scenarios linked to
tests via `Covers:` comments and verified by a coverage script.
