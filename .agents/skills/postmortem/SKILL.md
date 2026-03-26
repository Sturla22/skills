---
name: postmortem
description: Run a structured blameless postmortem after an incident, outage, or significant unexpected failure. Use when a production issue occurred, a fleet-wide update failed, a safety-critical bug escaped, or a systemic process failure needs learning capture.
allowed-tools: Read, Grep, Glob, Bash
---

# Postmortem

Extract durable lessons from incidents without blame.

## Process

1. **Establish timeline** — reconstruct what happened in chronological order. Use logs, commits, chat history, and operator testimony. Note times in UTC.
2. **Identify contributing factors** — list all factors that contributed to the incident. Avoid "root cause" singular — incidents almost always have multiple contributing causes (technical, process, communication, tooling).
3. **Classify impact** — scope (which users/devices/systems), duration, severity, data loss or corruption, safety implications.
4. **Map detection and response** — how was the incident detected? How long between occurrence, detection, and resolution? What worked well in the response?
5. **Extract lessons** — what did we learn? What assumptions were wrong? What safeguards were missing or bypassed?
6. **Define action items** — each action item must have an owner, a concrete deliverable, and a target date. Distinguish quick fixes (apply now) from systemic improvements (schedule in backlog).
7. **Review and publish** — review the postmortem with the team. Store the final record durably.

## Blameless principles

- Focus on systems and processes, not individuals.
- Assume people made reasonable decisions given the information they had at the time.
- "Who" is relevant only to understand what information was available, not to assign fault.
- Blame discourages honesty; honesty is the prerequisite for learning.

## Contributing factor categories

- **Technical** — missing validation, race condition, resource exhaustion, untested failure path
- **Process** — skipped review, missing test, unclear ownership, no runbook
- **Communication** — alert not routed, status unclear, handoff dropped
- **Tooling** — flaky CI, missing observability, misleading dashboard
- **Environment** — hardware failure, vendor outage, unexpected load

## Guardrails

- Do not publish a postmortem without action items — learning without follow-through is theater.
- Do not let action items go untracked — create work packets or backlog items with owners.
- Do not skip the timeline — accurate sequencing often reveals the real contributing factors.
- Do not conflate "what happened" with "what should have happened" — separate facts from judgments.

## Relation to agent failure notes

Agent failure notes (stored under `docs/workflow-experiments/`) capture AI-agent-specific misbehavior and guardrails. Postmortems cover broader production incidents, fleet failures, and systemic process breakdowns. Use agent failure notes for AI-specific issues; use postmortems for everything else.

## Done-when

- timeline is reconstructed with key events and timestamps
- contributing factors are identified (multiple, not just "root cause")
- impact is classified
- action items have owners and deliverables
- postmortem is stored durably

## Output

- incident timeline
- contributing factors
- impact classification
- detection and response assessment
- lessons learned
- action items with owners
