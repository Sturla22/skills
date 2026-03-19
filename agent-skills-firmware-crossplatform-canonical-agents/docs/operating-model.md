# Operating Model

## Principle

Keep one human-facing control thread. Specialist agents are internal workers, not separate personalities.

## Suggested loop

1. Planner scopes the task and names the evidence required.
2. Developer makes the smallest change that could work.
3. Verifier checks the claim independently.
4. Reviewer attacks the plan and patch.
5. Firmware-architect is brought in for HAL, contracts, migration, or structure-heavy work.

## Escalation rules

Bring in **firmware-architect** when:
- a hardware seam is missing
- platform code is leaking upward
- a migration path is unclear
- interface stability matters more than immediate speed
- the change affects timing, concurrency, or long-term architecture

Bring in **verifier** early when:
- the bug is not reproducible
- the test seam is unclear
- hardware availability is limited
- the change is risky or safety-sensitive

Bring in **reviewer** early when:
- the plan feels large
- multiple abstractions are being introduced
- the change crosses platform boundaries
- there is a temptation to "rewrite it cleanly"

## Anti-patterns

- letting the implementer declare victory
- doing hardware-only debugging when a deterministic host repro is possible
- introducing an abstraction before naming its real pressure
- widening scope because "we are already in the file"
- treating resource issues as post-processing

## Cross-tool note

The same role model is shared across Claude Code, GitHub Copilot, and OpenAI Codex.

- Edit canonical role definitions under `.agents/agents/*.toml`
- Edit canonical shared skills under `.agents/skills/`
- Regenerate downstream files with `python3 scripts/sync_agent_layouts.py`

Keep the role names and skill names aligned even when the native file formats differ, so prompts and handoffs stay portable.
