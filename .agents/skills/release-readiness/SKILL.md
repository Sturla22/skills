---
name: release-readiness
description: Prepare or assess a release using explicit SemVer classification, release shape, evidence gates, curated release communication, and concrete release inputs. Use when version bump, pre-release versus full release, changelog shaping, release blockers, or go/no-go decisions need a repeatable workflow.
allowed-tools: Read, Grep, Glob, Bash
---

# Release Readiness

Treat release preparation as a decision with evidence, not as a packaging afterthought.

## Process

1. **Read the contract and evidence** — use the work packet and `CHANGELOG.md` as the primary truth.
   ```
   Read("docs/work/<work-id>/brief.md"), Read("docs/work/<work-id>/plan.md"), Read("docs/work/<work-id>/status.md"), Glob("docs/work/<work-id>/evidence/**"), Read("CHANGELOG.md")
   ```

2. **Identify the release candidate inputs** — name the exact commit or tag to release, the key artifacts, and any digest or provenance evidence available. If the candidate itself is fuzzy, the release is not ready.

3. **Classify the contract impact** — compare the observed change against the documented public contract and state `MAJOR`, `MINOR`, `PATCH`, pre-release only, or no release impact. If the contract changed incompatibly, do not soften the bump.

4. **Choose the release shape honestly** — decide whether the current evidence supports a full release, a pre-release, a canary or staged rollout, or no release yet. Match the rollout shape to the actual risk profile rather than habit.

5. **Check the gates** — make the required gates explicit:
   - verification evidence is present
   - unresolved blockers are named
   - migration or deprecation guidance exists when users must adapt
   - `CHANGELOG.md` and release notes reflect the real change
   - missing hardware or integration evidence is called out instead of hidden

6. **Curate the release communication** — keep `CHANGELOG.md` human-readable and update release notes with the things downstream readers actually need: breaking changes, deprecations, migrations, notable fixes, and known gaps. Generated notes may help draft, but they do not replace curation.

7. **Make the go / no-go call explicit** — summarize what is ready, what is blocked, what kind of release is honest right now, and what must happen next if the answer is "not yet."

## Guardrails
- Do not treat raw commit history as sufficient release communication.
- Do not label a build as final when a pre-release is the more honest description.
- Do not release with unresolved blockers hidden behind vague wording.
- Do not modify the contents of an already released version; publish a new version instead.
- Do not claim a non-breaking bump if the documented contract actually changed incompatibly.
- If artifact identity, provenance, or target commit is unknown, stop and resolve that first.

## When release prep stalls
- **SemVer is disputed** — compare the observed change to the documented contract, not to intent alone.
- **Evidence is incomplete** — route missing proof to `verifier` or `integration-engineer`.
- **The changelog is noisy** — rewrite for readers; group by notable change type and remove commit-log noise.
- **Migration impact is unclear** — involve `technical-writer` or `firmware-architect` before cutting the release.

## Done-when
- the version impact is explicit
- the release shape is explicit
- candidate inputs and gates are explicit
- changelog and release notes match the evidence
- blockers and known gaps are stated honestly

## Output
- candidate inputs
- SemVer or pre-release classification
- release shape
- gate status
- changelog / release-note updates
- blockers and missing evidence
- go / no-go recommendation
