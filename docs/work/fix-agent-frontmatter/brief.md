# Product Brief

## Storage

- Work ID: `fix-agent-frontmatter`
- File path: `docs/work/fix-agent-frontmatter/brief.md`

## Request summary

Fix custom agent files that fail to load because their markdown frontmatter is malformed.

## Problem / desired outcome

Agent definitions in `.github/agents/` should parse and load successfully. The current files fail YAML frontmatter parsing because plain-scalar `description` values include `:` characters.

## Why this matters

Broken custom agents make the repo's documented role flow unavailable and degrade the intended workflow.

## Code drivers

- Risk — addresses a known workflow failure in repo automation
- Design intent communication — preserves the documented custom-agent contract

## Stakeholders / users

- Repo maintainers
- Contributors using the custom agent set

## Stakeholder needs / system outcomes

- Custom agents load reliably
- Agent prompt bodies remain unchanged

## Design criteria / key parameters

- Smallest effective diff
- No behavior changes beyond valid parsing

## In scope

- `.github/agents/*.agent.md` frontmatter fixes required for valid YAML

## Out of scope

- Prompt-body rewrites
- Role or workflow redesign

## Constraints

- Preserve existing agent names, models, and prompt content
- Keep the fix easy to audit

## Existing conventions to preserve

- Existing agent file layout and naming
- Existing role descriptions and prompt text

## System context / external interfaces

- GitHub Copilot custom agent markdown frontmatter under `.github/agents/`

## Acceptance criteria

- Every custom agent file has YAML frontmatter that parses cleanly
- Agent descriptions preserve their original wording
- No non-frontmatter content changes are introduced

## Behavior scenarios (BDD)

- Given a custom agent file with a `description` containing `:`
- When the frontmatter is parsed as YAML
- Then parsing succeeds and the agent remains loadable

## Public contract / compatibility impact

- No intentional contract change

## Delivery class

- Non-productized tool / workflow fix

## TDD expectation

- TDD not required for this configuration-only fix; parser-based verification replaces it

## Validation intent / evidence

- Not a separate concern for this slice

## SemVer / changelog expectation

- No changelog update expected for this local workflow repair

## Assumptions

- The reported load failures all stem from the same YAML plain-scalar issue

## Open questions

- None at this time

## Recommended next owner(s)

- Developer
- Verifier

## Parallelization notes

- Not needed; one write lane covers the whole change safely

## Delegation notes

- Keep the diff frontmatter-only unless validation reveals another loader issue
