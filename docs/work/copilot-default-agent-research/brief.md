# Product Brief

## Storage

- Work ID: `copilot-default-agent-research`
- File path: `docs/work/copilot-default-agent-research/brief.md`

## Request summary

Research whether GitHub Copilot can be made to default to the `product-owner` custom agent for this repository, similar to the Claude-side default behavior.

## Problem / desired outcome

Establish, from authoritative sources and repo evidence, whether GitHub Copilot supports a repo-level default custom agent selection and whether this repo can make `product-owner` the default Copilot agent.

## Why this matters

The repo currently documents a product-owner front door. If Copilot cannot enforce that at runtime, the repo should distinguish between documented workflow guidance and actual tool-supported defaults.

## In scope

- Research current Copilot CLI and repo-supported configuration for default agent behavior
- Compare runtime-enforced defaults with instruction-driven behavior

## Out of scope

- Implementing workflow changes
- Redesigning the role model

## Acceptance criteria

- Research findings are anchored to authoritative sources
- The answer distinguishes enforced runtime settings from instruction-only guidance
- Gaps and unknowns are made explicit

## Delivery class

- Non-productized tool / workflow research

## TDD expectation

- Not applicable; source-based verification is the required evidence
