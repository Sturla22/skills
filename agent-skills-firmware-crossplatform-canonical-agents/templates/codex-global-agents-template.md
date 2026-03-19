# ~/.codex/AGENTS.md template

## Personal working agreements

- Prefer the smallest effective diff.
- Run the strongest focused verification available after edits.
- Ask before adding new dependencies or changing public interfaces.
- State clearly what was not verified.
- Prefer remove-before-add and inline-before-abstract for cleanup work.

## Embedded firmware defaults

- Make units, timing assumptions, ownership, and failure behavior explicit.
- Prefer simulation or host tests before hardware-only debugging when practical.
- Be conservative with blocking behavior, retries, logging volume, and dynamic allocation.
