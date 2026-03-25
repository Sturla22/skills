# Work Plan

## Problem statement

Provide a low-friction way to start Copilot with the repo's intended `product-owner` entrypoint.

## Approach

1. Add a small Python launcher under `tools/dev/`.
2. Keep the launcher narrow: inject `--agent product-owner`, pass other args through, and reject conflicting `--agent` input.
3. Add focused pytest coverage for command construction.
4. Add a short usage note in the existing Copilot documentation.
