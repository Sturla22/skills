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
)

EVIDENCE_HINTS = (
    "check",
    "test",
    "verified",
    "risk",
    "blocker",
    "assumption",
    "residual",
    "unverified",
    "docs/work/",
    "brief.md",
    "plan.md",
    "status.md",
    "handoff",
    "evidence",
)


def main() -> int:
    event = load_event()
    if event.get("stop_hook_active"):
        return 0

    message = str(event.get("stop_hook_data", {}).get("stop_hook_result", "")).lower()
    if not message:
        return 0

    if has_any(message, COMPLETION_HINTS) and not has_any(message, EVIDENCE_HINTS):
        emit_block(
            "Before stopping, leave a tighter worker result: what you changed or found, checks run, residual risk or blockers, and any work-packet file updates or pointers. Then stop."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
