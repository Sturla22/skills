# Product Brief

## Storage

- Work ID: `copilot-product-owner-launcher`
- File path: `docs/work/copilot-product-owner-launcher/brief.md`

## Request summary

Add a small repo-owned script that starts GitHub Copilot CLI in the intended `product-owner` flow.

## Problem / desired outcome

Copilot does not currently appear to offer a repo-level setting that forces the default selected custom agent to `product-owner`. The repo therefore needs a simple, explicit launcher that consistently starts Copilot with that agent selected.

## Why this matters

The repo's operating model assumes a `product-owner` front door for non-trivial work. A launcher reduces friction and avoids relying on each user to remember the correct startup flags.

## In scope

- Add a small launcher script
- Add focused verification
- Add a short usage note in existing docs

## Out of scope

- Changing Copilot's runtime behavior beyond the launcher
- Redesigning the role model

## Acceptance criteria

- A repo-owned command starts `copilot` with `--agent product-owner`
- Normal Copilot arguments still pass through
- Conflicting explicit `--agent` overrides are rejected clearly
- The new behavior is documented briefly

## Delivery class

- Non-productized tool

## TDD expectation

- Lightweight test-first verification is appropriate for this repo-owned helper
