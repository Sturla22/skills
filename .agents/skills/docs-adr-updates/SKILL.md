---
name: docs-adr-updates
description: Keep README, CHANGELOG, architecture notes, and ADRs aligned with the implemented system. Use when a design decision changed, an interface or API changed, a migration path was introduced, docs are stale, release-facing behavior changed, or an ADR needs to be written or updated after implementation.
allowed-tools: Read, Grep, Glob, Bash
---

# Docs and ADR Updates

Keep written design truth aligned with code.

## Process

1. **Find all docs** — locate README, `CHANGELOG.md`, ADR directory, architecture notes, and inline design docs.
   ```
   Glob("**/{README*,CHANGELOG.md,CLAUDE.md,docs/**,adr/**,decisions/**,*.md}")
   ```

2. **Identify stale content** — grep for symbols, interface names, or module names that changed.
   ```
   Grep("<changed-symbol>", glob="**/*.md")
   ```

3. **Identify audience and doc form** — decide whether each update is best expressed as tutorial, how-to, reference, explanation, release note, changelog entry, or ADR. Prefer one recommended path for task docs unless multiple paths are materially necessary.

4. **Update minimum set** — edit only docs that now contradict the implementation or leave readers without the guidance they now need; leave unrelated docs untouched.

5. **Write or update the ADR** — if no ADR exists for this decision, create one. Use the MADR structure (required fields):
   - `Title` — encodes both the problem and solution chosen (not just the solution)
   - `Context and Problem Statement` — 2–3 sentences; what forced this decision?
   - `Decision Drivers` — bulleted quality attributes or constraints
   - `Considered Options` — at least two genuine alternatives at the same abstraction level
   - `Decision Outcome` — chosen option + one concrete reason
   - `Consequences` — explicit "Good, because…" AND at least one "Bad, because…"

6. **Handle superseding** — if this decision replaces an earlier one: set old ADR status to `Superseded by ADR-NNN`, cross-link both, and leave the old ADR in the repo (the historical chain is the value).

7. **Update the changelog when notable** — if the change affects the documented contract or matters to downstream users, update `CHANGELOG.md` under `Unreleased` using a curated Keep a Changelog heading such as `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, or `Security`.

8. **Note migration** — add a migration note if callers or dependents need to adapt.

9. **State versioning impact when relevant** — if the documented contract changed, note whether the release implication is `MAJOR`, `MINOR`, or `PATCH`, and make sure deprecations are documented before removals when practical.

10. **Make the doc usable** — keep long-lived product docs timeless unless the content is intentionally release-specific; use explicit versions or dates for release notes and changelog entries. Make headings, link text, examples, and procedures easy to scan and accessible. Avoid visual-only cues or fuzzy time words like "currently" or "recently" in durable docs.

## ADR quality guardrails
- Every ADR must have at least one "Bad, because…" in Consequences — if everything is good, it is a Sales Pitch, not an analysis.
- List only genuine alternatives — dummy options that obviously fail invalidate the analysis.
- Do not delete or edit accepted ADRs in place; create a new one to change a decision.
- Keep ADRs decision-focused — no implementation details that belong in code comments.
- Store ADRs in the repo alongside the code they describe, not in a separate wiki.
- Do not dump raw commit summaries into `CHANGELOG.md`; curate for downstream readers.
- Do not duplicate volatile work-packet detail in long-lived docs when a stable reference is clearer.
- Do not create multiple overlapping procedures when one recommended path will serve most readers.

## Common ADR anti-patterns to avoid
- **Fairy Tale / Wishful Thinking** — only pros listed, no cons.
- **Sales Pitch** — marketing language with no evidence.
- **Sprint (Rush)** — only immediate effects; no long-term consequences considered.
- **Dummy Alternative** — fake options listed to make the chosen option look obviously right.
- **Mega-ADR** — multi-page document; an ADR is a decision record, not architecture documentation.

## When alignment is unclear
- **Docs and code both seem valid** — flag the ambiguity; ask which is authoritative.
- **No ADR directory exists** — create `docs/adr/` and note the convention in README.
- **Change is too large to document fully** — document the interface contract; leave implementation details to code.
- **Unsure whether the change is changelog-worthy** — ask whether a downstream user of the documented repo contract would care.
- **Docs are accurate but hard to use** — reorganize by reader need: tutorial, how-to, reference, explanation.

## Done-when
- code and docs no longer contradict
- release-facing changes are reflected in `CHANGELOG.md` when relevant
- key decisions are recorded with options and consequences
- future readers can understand the intended design
- the doc form and audience are clear

## Output
- docs updated
- audience and content form
- changelog updated when relevant
- stale assumptions removed
- decisions recorded (MADR structure)
- migration notes
