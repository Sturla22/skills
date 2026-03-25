# Product Brief

## Storage

- Work ID: `copilot-small-patch-bias`
- File path: `docs/work/copilot-small-patch-bias/brief.md`

## Request summary

Discourage GitHub Copilot from attempting oversized patches that often fail, by strengthening the repo's Copilot-facing guidance.

## Problem / desired outcome

Copilot has a tendency to attempt large patch sets in one jump, then fail or thrash. The desired outcome is a small workflow adjustment that biases Copilot toward narrow, staged patches and smaller write surfaces.

## Why this matters

Oversized patches increase failure rate, reduce reviewability, and make it harder for Copilot to recover when an edit attempt does not apply cleanly.

## In scope

- Tighten Copilot-specific repo instructions
- Record the workflow experiment
- Update the changelog

## Out of scope

- Role redesign
- New skill creation
- Broad multi-surface workflow rewrite

## Acceptance criteria

- Copilot-facing repo guidance explicitly prefers narrow, staged patches
- The change stays focused on Copilot-facing guidance rather than broad operating-model churn
- The workflow experiment and changelog capture the contract change

## Delivery class

- Non-productized workflow change

## TDD expectation

- Not applicable; prompt/docs review is the verification path for this slice
