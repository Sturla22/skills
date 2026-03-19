#!/usr/bin/env python3
from __future__ import annotations

from common import emit_block, has_any, load_event

COMPLETION_HINTS = (
    "done",
    "complete",
    "completed",
    "finished",
    "implemented",
    "updated",
    "changed",
    "added",
    "verified",
    "reviewed",
    "fixed",
)

FINALIZATION_HINTS = (
    "what changed",
    "verified",
    "residual",
    "risk",
    "unverified",
    "docs/work/",
    "brief.md",
    "plan.md",
    "status.md",
    "handoff",
    "evidence",
    "changelog",
)


def main() -> int:
    event = load_event()
    if event.get("stop_hook_active"):
        return 0

    message = str(event.get("stop_hook_data", {}).get("stop_hook_result", "")).lower()
    if not message:
        return 0

    if has_any(message, COMPLETION_HINTS) and not has_any(message, FINALIZATION_HINTS):
        emit_block(
            "Before stopping, add a concise closeout with what changed, what was verified, residual risk or gaps, and whether the work packet, handoff, or evidence files were updated for non-trivial work. Then stop."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
