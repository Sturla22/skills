---
name: research
description: Conduct structured external domain investigation and produce a durable research summary. Use when a knowledge gap must be closed before planning is possible — datasheets, specs, standards, errata, feasibility signals, technology landscape. Stops before option comparison or task framing begins.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Research

Close a specific external knowledge gap and return a durable, scoped summary.

## Process

1. **Restate the research question precisely** — before searching, write the question in one or two sentences. If it is compound, split it into sub-questions and note the dependency order.

2. **Identify minimum necessary sources** — prefer primary sources:
   - datasheets and application notes (manufacturer site, archive.org)
   - standards and specifications (issuing body, numbered version)
   - errata and silicon revision notes (manufacturer's errata list)
   - vendor SDK or HAL release notes when the question is integration-specific
   - secondary sources only when primary sources are unavailable; flag this clearly

3. **Fetch and read sources systematically**
   ```
   WebFetch(url) — primary source fetch
   WebSearch(query) — locate sources when the URL is unknown
   Read(path) — local docs, datasheets checked into the repo
   ```
   Record title, URL or path, document version, and retrieval date for each source consulted.

4. **Extract and anchor findings** — for each key finding:
   - quote or paraphrase the relevant passage
   - cite the source, version, and section number
   - note whether the finding is definitive or inferred

5. **Flag gaps and ambiguities explicitly**
   - items not answerable from available sources
   - conflicts between sources (e.g., datasheet vs. errata)
   - findings that depend on a specific device revision, silicon stepping, or standard version
   - items that need hardware confirmation or vendor clarification

6. **State the research boundary** — write one explicit sentence marking where the facts end and design decisions begin. Do not cross this line.

7. **Produce the durable research summary** at `docs/work/<work-id>/evidence/research-<topic>.md`:
   ```markdown
   # Research: <topic>

   **Research question:** <one or two sentences>
   **Retrieval date:** <YYYY-MM-DD>

   ## Key findings
   | Finding | Source | Version | Section |
   |---------|--------|---------|---------|
   | ...     | ...    | ...     | ...     |

   ## Gaps and open items
   - <item needing hardware or vendor confirmation>
   - <conflict between sources>

   ## Research boundary
   Facts established above. Design options and trade-offs begin here — hand to planner.
   ```

## Guardrails
- Do not produce a plan, architecture, or recommendation list.
- Do not resolve a source conflict by choosing a side without flagging it.
- Do not treat a secondary blog post or forum thread as a primary source without noting the limitation.
- Do not leave findings uncited or unanchored to a specific document version.
- Do not widen the research question without returning to product-owner first.
- Do not continue if the question is too broad for the turn budget — narrow it, answer the narrowed form, and return the remainder as a gap.
- Do not speculate about design implications; return facts and stop.

## When research stalls
- **Source not found** — record what was searched, what was not found, and suggest a vendor contact or alternate source.
- **Conflicting sources** — present both, note which is more authoritative and why, and flag for human resolution.
- **Question too broad** — narrow to the highest-priority sub-question, answer it, and note the others as gaps.
- **Primary source behind a login or NDA** — note the access barrier and suggest what the team needs to obtain it.

## Done-when
- the research question is restated precisely
- all consulted sources are cited with title, version, and retrieval date
- key findings are anchored to specific source sections
- gaps, conflicts, and items needing hardware or vendor confirmation are listed
- the research boundary is stated explicitly
- the durable summary file is written to `docs/work/<work-id>/evidence/`

## Output
- path to the durable research summary
- executive summary (one paragraph)
- gaps requiring hardware, vendor, or specialist confirmation
- explicit research boundary statement
