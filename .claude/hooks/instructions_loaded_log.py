#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone

from common import load_event, project_root


def main() -> int:
    event = load_event()
    root = project_root(event)
    log_dir = root / ".claude" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "instructions-loaded.jsonl"

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hook_event_name": event.get("hook_event_name"),
        "session_id": event.get("session_id"),
        "transcript_path": event.get("transcript_path"),
        "cwd": event.get("cwd"),
    }

    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True))
        handle.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
