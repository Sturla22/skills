#!/usr/bin/env python3
from __future__ import annotations

from common import emit_additional_context, load_event


def main() -> int:
    event = load_event()
    emit_additional_context(
        str(event.get("hook_event_name", "PreCompact")),
        "Before compaction, preserve only the durable pointers and current control state: current work packet path; brief.md, plan.md, and status.md; current owner, lane, and worktree or other isolation; active evidence files; open risks; and the next action.",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
