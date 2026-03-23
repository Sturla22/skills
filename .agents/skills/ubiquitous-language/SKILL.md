---
name: ubiquitous-language
description: Extract domain terminology from conversation or documentation into a canonical glossary so the same term always means the same thing across code, tests, docs, and AI prompts. Use when starting a new domain, when terminology confusion is causing miscommunication, or when reviewing code that mixes synonyms for the same concept.
allowed-tools: Read, Grep, Glob, Bash
---

# Ubiquitous Language

Establish a shared vocabulary. One term, one meaning, everywhere.

## Process

1. **Scan for domain terms.** Read the conversation, brief, and any provided documents. Look for: domain-relevant nouns, verbs, and concepts. Look especially for:
   - Same word used for different concepts (ambiguity)
   - Different words for the same concept (synonyms)
   - Vague or overloaded terms with context-dependent meaning

2. **Propose a canonical glossary.** Be opinionated: pick the best term for each concept, list the alternatives as aliases to avoid.

3. **Include relationships.** For the most important terms, note the relationships between them with cardinality (e.g., "a Session has one or more Events"; "a Controller reads from exactly one Sensor").

4. **Include example dialogue.** Write 3–5 short exchanges between a developer and a domain expert demonstrating precise term usage. This tests whether the definitions are usable in practice.

5. **Flag ambiguities.** Explicitly name terms where the right choice is unclear or contested.

6. **Write the glossary.** Write to `docs/ubiquitous-language.md` for repo-level glossaries, or `docs/work/<work-id>/ubiquitous-language.md` for work-scoped glossaries.

7. **State the commitment.** After writing the file, say: "From this point forward I will use these terms consistently."

## Glossary format

```markdown
## <Domain Cluster Name>

| Term | Definition | Aliases to avoid |
|------|-----------|-----------------|
| <term> | <one sentence: what it IS, not what it does> | <synonym1>, <synonym2> |

## Relationships

- <Term A> has one or more <Term B>s
- <Term C> belongs to exactly one <Term D>

## Example dialogue

**Developer:** "Does the controller process each reading independently?"
**Domain expert:** "No — the controller accumulates samples into a window before producing an output."

## Flagged ambiguities

- "<term>": used to mean both X and Y in current docs; decision needed
```

## Re-running

When run on a codebase that already has a glossary file:
- Read the existing file first.
- Incorporate new terms found in the current scan.
- Update changed definitions (mark them "(updated)").
- Mark new entries "(new)".
- Re-flag new ambiguities.
- Rewrite the example dialogue if new terms change the conversation shape.

## Guardrails

- Be opinionated: pick the best term and list alternatives as aliases to avoid. Do not present all synonyms as equally valid.
- Keep definitions to one sentence: define what it IS, not what it does.
- Only include domain terms — not generic programming concepts (no "function", "variable", "module").
- Group by natural domain clusters, not alphabetically.
- Do not add a term just because it appears frequently — add it because its meaning needs to be pinned.

## Done-when

- The glossary file exists at the target path.
- Each significant domain term has a canonical name, a one-sentence definition, and aliases to avoid.
- Key relationships are stated with cardinality.
- Example dialogue demonstrates the vocabulary in use.
- Ambiguities are flagged explicitly.

## Output

- Glossary file written (path)
- Summary of terms added, updated, and flagged
- Commitment statement
