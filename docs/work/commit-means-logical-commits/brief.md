# Product Brief

## Storage

- Work ID: `commit-means-logical-commits`
- File path: `docs/work/commit-means-logical-commits/brief.md`

## Request summary

Clarify the operating model so that a bare user request to "commit" means creating logical commits rather than forcing everything into one umbrella commit.

## Problem / desired outcome

The repo already prefers logical, atomic commits, but it does not explicitly say how agents should interpret a plain user request like "commit." The desired outcome is a clearer operating-model rule: unless the user explicitly asks for one squashed commit, "commit" authorizes one or more logical commits.

## Why this matters

Without this clarification, the agent can interpret "commit" too literally and collapse multiple logical changes into one commit, reducing reviewability and history quality.

## In scope

- Update the operating-model contract
- Record the workflow experiment
- Update the changelog

## Out of scope

- Changing git tooling
- Adding a new role or skill

## Acceptance criteria

- The operating model explicitly states how to interpret a bare "commit" request
- The rule preserves the preference for logical, atomic commits
- The changelog and workflow-experiment record reflect the contract change

## Delivery class

- Non-productized workflow change

## TDD expectation

- Not applicable; doc and contract verification is the required evidence
