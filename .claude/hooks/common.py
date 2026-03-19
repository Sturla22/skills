from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def load_event() -> dict:
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def emit(payload: dict) -> None:
    json.dump(payload, sys.stdout)
    sys.stdout.write("\n")


def emit_additional_context(event_name: str, text: str) -> None:
    emit(
        {
            "hookSpecificOutput": {
                "hookEventName": event_name,
                "additionalContext": text,
            }
        }
    )


def emit_block(reason: str) -> None:
    emit({"decision": "block", "reason": reason})


def project_root(event: dict) -> Path:
    root = os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or "."
    return Path(root).resolve()


def has_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)
