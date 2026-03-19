#!/usr/bin/env python3
from __future__ import annotations

from common import emit_additional_context, has_any, load_event

NON_TRIVIAL_HINTS = (
    "feature",
    "bug",
    "fix",
    "refactor",
    "plan",
    "workflow",
    "role",
    "skill",
    "agent",
    "release",
    "integration",
    "parallel",
    "worktree",
    "architecture",
    "research",
    "verify",
    "changelog",
    "semver",
)

ALREADY_ROUTED_HINTS = (
    "product-owner",
    "docs/work/",
    "work packet",
    "brief.md",
    "plan.md",
    "status.md",
)


def main() -> int:
    event = load_event()
    prompt = str(event.get("prompt", "")).strip()
    prompt_lower = prompt.lower()

    if not prompt:
        return 0

    if has_any(prompt_lower, ALREADY_ROUTED_HINTS):
        return 0

    if len(prompt_lower) < 40 and not has_any(prompt_lower, NON_TRIVIAL_HINTS):
        return 0

    reminders = [
        "Repo workflow reminder: for non-trivial work, stay in the product-owner control thread first and keep durable context under docs/work/<work-id>/brief.md, plan.md, and status.md."
    ]

    if has_any(prompt_lower, ("parallel", "lane", "worktree")):
        reminders.append(
            "If this splits into parallel lanes, have planner define ownership boundaries, merge points, and worktree names or other isolation before implementation starts."
        )

    if has_any(prompt_lower, ("claude", "hook", "rule", "mcp", "output style")):
        reminders.append(
            "Claude-native runtime files live in .claude/settings.json, .claude/rules/, .claude/hooks/, .claude/output-styles/, and .mcp.json; keep shared role and skill logic in .agents/."
        )

    emit_additional_context("UserPromptSubmit", " ".join(reminders))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
