#!/usr/bin/env python3
"""scripts/cli.py — scaffolding and inspection CLI for this repo.

All subcommands exit 0 on success, non-zero on error.
No ANSI colour codes. No interactive prompts. No pip dependencies.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Repo-root detection
# ---------------------------------------------------------------------------

def _repo_root() -> Path:
    """Return the repo root by walking up from this script's location."""
    here = Path(__file__).resolve().parent
    # scripts/ lives one level below the repo root
    return here.parent


ROOT = _repo_root()
TEMPLATES_DIR = ROOT / "templates"
DOCS_WORK_DIR = ROOT / "docs" / "work"
AGENTS_AGENTS_DIR = ROOT / ".agents" / "agents"
AGENTS_SKILLS_DIR = ROOT / ".agents" / "skills"

SYNC_REMINDER = (
    "Reminder: run `python scripts/sync_agent_layouts.py` "
    "to propagate changes to .claude/, .github/, and .codex/ layouts."
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _read_template(name: str) -> str:
    path = TEMPLATES_DIR / name
    if not path.exists():
        print(f"ERROR: template not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def _write_new_file(dest: Path, content: str) -> None:
    """Write content to dest; exit 1 if dest already exists."""
    if dest.exists():
        print(f"ERROR: already exists: {dest}", file=sys.stderr)
        sys.exit(1)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    print(f"Created: {dest}")


# ---------------------------------------------------------------------------
# Subcommand: new-work  (SC-001)
# ---------------------------------------------------------------------------

def cmd_new_work(args: argparse.Namespace) -> None:
    work_id: str = args.work_id
    packet_dir = DOCS_WORK_DIR / work_id

    if packet_dir.exists():
        print(f"ERROR: already exists: {packet_dir}", file=sys.stderr)
        sys.exit(1)

    packet_dir.mkdir(parents=True)
    (packet_dir / "handoffs").mkdir()
    (packet_dir / "evidence").mkdir()

    template_map = {
        "product-brief-template.md": "brief.md",
        "work-plan-template.md": "plan.md",
        "work-status-template.md": "status.md",
    }
    for tmpl_name, dest_name in template_map.items():
        content = _read_template(tmpl_name)
        content = content.replace("<work-id>", work_id)
        dest = packet_dir / dest_name
        dest.write_text(content, encoding="utf-8")
        print(f"Created: {dest}")

    print(f"Created: {packet_dir / 'handoffs'}/")
    print(f"Created: {packet_dir / 'evidence'}/")
    print(f"Work packet scaffolded at: {packet_dir}")


# ---------------------------------------------------------------------------
# Subcommand: new-scenarios  (SC-002)
# ---------------------------------------------------------------------------

def cmd_new_scenarios(args: argparse.Namespace) -> None:
    content = _read_template("scenarios-template.md")

    if args.work:
        dest = DOCS_WORK_DIR / args.work / "scenarios.md"
    else:
        dest = ROOT / "docs" / "scenarios.md"

    _write_new_file(dest, content)


# ---------------------------------------------------------------------------
# Subcommand: new-handoff  (SC-003)
# ---------------------------------------------------------------------------

def cmd_new_handoff(args: argparse.Namespace) -> None:
    work_id: str = args.work_id
    from_role: str = args.from_role
    to_role: str = args.to_role

    packet_dir = DOCS_WORK_DIR / work_id
    if not packet_dir.exists():
        print(f"ERROR: work packet not found: {packet_dir}", file=sys.stderr)
        sys.exit(1)

    handoffs_dir = packet_dir / "handoffs"
    if not handoffs_dir.exists():
        print(f"ERROR: handoffs directory not found: {handoffs_dir}", file=sys.stderr)
        sys.exit(1)

    # Scan for existing NNN-* files to determine next sequence number
    existing = [
        p.name for p in handoffs_dir.iterdir()
        if p.is_file() and re.match(r"^\d{3}-", p.name)
    ]
    if existing:
        max_seq = max(int(name[:3]) for name in existing)
        seq = max_seq + 1
    else:
        seq = 1

    seq_str = f"{seq:03d}"
    filename = f"{seq_str}-{from_role}-to-{to_role}.md"
    dest = handoffs_dir / filename

    content = _read_template("handoff-template.md")
    # Pre-fill structural placeholders
    content = content.replace("<work-id>", work_id)
    content = content.replace("<sequence>", seq_str)
    content = content.replace("<from>", from_role)
    content = content.replace("<to>", to_role)

    _write_new_file(dest, content)


# ---------------------------------------------------------------------------
# Subcommand: check-work  (SC-004)
# ---------------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"<[^>]+>")


def _extract_sections(text: str) -> list[tuple[str, str]]:
    """Return list of (heading, body) pairs for all ## sections."""
    lines = text.splitlines()
    sections: list[tuple[str, str]] = []
    current_heading: str | None = None
    current_body_lines: list[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, "\n".join(current_body_lines)))
            current_heading = line[3:].strip()
            current_body_lines = []
        elif current_heading is not None:
            current_body_lines.append(line)

    if current_heading is not None:
        sections.append((current_heading, "\n".join(current_body_lines)))

    return sections


def _section_is_incomplete(body: str) -> bool:
    stripped = body.strip()
    if not stripped:
        return True
    if _PLACEHOLDER_RE.search(stripped):
        return True
    return False


def cmd_check_work(args: argparse.Namespace) -> None:
    work_id: str = args.work_id
    packet_dir = DOCS_WORK_DIR / work_id

    if not packet_dir.exists():
        print(f"ERROR: work packet not found: {packet_dir}", file=sys.stderr)
        sys.exit(1)

    incomplete: list[str] = []

    for fname in ("brief.md", "status.md"):
        fpath = packet_dir / fname
        if not fpath.exists():
            print(f"ERROR: missing file: {fpath}", file=sys.stderr)
            sys.exit(1)
        text = fpath.read_text(encoding="utf-8")
        sections = _extract_sections(text)
        for heading, body in sections:
            if _section_is_incomplete(body):
                incomplete.append(f"{fname}: ## {heading}")

    if incomplete:
        print(f"INCOMPLETE: {work_id} has {len(incomplete)} unfilled section(s):")
        for item in incomplete:
            print(f"  - {item}")
        sys.exit(1)
    else:
        print(f"OK: {work_id} — all required sections are filled.")


# ---------------------------------------------------------------------------
# Subcommand: list-work  (SC-005)
# ---------------------------------------------------------------------------

def _parse_status(status_path: Path) -> tuple[str, str]:
    """Return (owner, step) by line-scanning status.md.

    Returns ("unknown", "unknown") for any field that cannot be parsed.
    """
    owner = "unknown"
    step = "unknown"

    if not status_path.exists():
        return owner, step

    lines = status_path.read_text(encoding="utf-8").splitlines()
    in_current_owner = False
    in_current_step = False
    found_step_heading = False

    for line in lines:
        stripped = line.strip()

        if stripped == "## Current owner":
            in_current_owner = True
            in_current_step = False
            found_step_heading = False
            continue

        if stripped == "## Current step":
            in_current_step = True
            in_current_owner = False
            found_step_heading = True
            continue

        # Any other ## heading resets state
        if stripped.startswith("## "):
            in_current_owner = False
            in_current_step = False
            continue

        if in_current_owner and stripped.startswith("- Role:"):
            value = stripped[len("- Role:"):].strip()
            if value:
                owner = value
            in_current_owner = False

        if in_current_step and found_step_heading and stripped:
            step = stripped
            in_current_step = False

    return owner, step


def cmd_list_work(args: argparse.Namespace) -> None:
    if not DOCS_WORK_DIR.exists():
        print("No work packets found.")
        return

    packets = sorted(
        p for p in DOCS_WORK_DIR.iterdir()
        if p.is_dir()
    )

    if not packets:
        print("No work packets found.")
        return

    for packet_dir in packets:
        work_id = packet_dir.name
        status_path = packet_dir / "status.md"
        owner, step = _parse_status(status_path)
        print(f"{work_id}  owner: {owner}  step: {step}")


# ---------------------------------------------------------------------------
# Subcommand: new-agent  (SC-006)
# ---------------------------------------------------------------------------

_TQ = '"""'
_AGENT_STUB_TMPL = (
    'name = "{name}"\n'
    'description = "# TODO: describe this agent"\n'
    'tools = []\n'
    'skills = []\n'
    'claude_max_turns = 20\n'
    'body = ' + _TQ + '\n'
    '# TODO: describe role responsibilities, optimizations, and return contract.\n'
    + _TQ + '\n'
)


def cmd_new_agent(args: argparse.Namespace) -> None:
    name: str = args.name
    dest = AGENTS_AGENTS_DIR / f"{name}.toml"

    content = _AGENT_STUB_TMPL.format(name=name)
    _write_new_file(dest, content)
    print(SYNC_REMINDER)


# ---------------------------------------------------------------------------
# Subcommand: new-skill  (SC-007)
# ---------------------------------------------------------------------------

_SKILL_STUB_TMPL = """\
---
name: {name}
description: "# TODO: describe this skill"
allowed-tools: []
---

# {title}

## Process

<!-- TODO: describe the process steps for this skill. -->

## Done-when

<!-- TODO: describe the completion criteria for this skill. -->

## Output

<!-- TODO: describe the expected output of this skill. -->
"""


def cmd_new_skill(args: argparse.Namespace) -> None:
    name: str = args.name
    title = name.replace("-", " ").title()
    skill_dir = AGENTS_SKILLS_DIR / name
    dest = skill_dir / "SKILL.md"

    content = _SKILL_STUB_TMPL.format(name=name, title=title)
    # _write_new_file handles parent mkdir
    if dest.exists():
        print(f"ERROR: already exists: {dest}", file=sys.stderr)
        sys.exit(1)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    print(f"Created: {dest}")
    print(SYNC_REMINDER)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cli.py",
        description=(
            "Scaffolding and inspection CLI for this repo. "
            "All commands exit 0 on success, non-zero on error."
        ),
    )
    sub = parser.add_subparsers(dest="command", metavar="<subcommand>")
    sub.required = True

    # new-work
    p_new_work = sub.add_parser(
        "new-work",
        help="Scaffold a new work packet under docs/work/<work-id>/",
    )
    p_new_work.add_argument("work_id", metavar="<work-id>", help="Work packet identifier")
    p_new_work.set_defaults(func=cmd_new_work)

    # new-scenarios
    p_new_scenarios = sub.add_parser(
        "new-scenarios",
        help="Create a scenarios.md file from template",
    )
    p_new_scenarios.add_argument(
        "--work",
        metavar="<work-id>",
        default=None,
        help="Place scenarios.md inside docs/work/<work-id>/ instead of docs/",
    )
    p_new_scenarios.set_defaults(func=cmd_new_scenarios)

    # new-handoff
    p_new_handoff = sub.add_parser(
        "new-handoff",
        help="Create the next numbered handoff file in a work packet",
    )
    p_new_handoff.add_argument("work_id", metavar="<work-id>", help="Work packet identifier")
    p_new_handoff.add_argument("--from", dest="from_role", required=True, metavar="<role>",
                                help="Source role")
    p_new_handoff.add_argument("--to", dest="to_role", required=True, metavar="<role>",
                                help="Destination role")
    p_new_handoff.set_defaults(func=cmd_new_handoff)

    # check-work
    p_check_work = sub.add_parser(
        "check-work",
        help="Check that all ## sections in brief.md and status.md are filled",
    )
    p_check_work.add_argument("work_id", metavar="<work-id>", help="Work packet identifier")
    p_check_work.set_defaults(func=cmd_check_work)

    # list-work
    p_list_work = sub.add_parser(
        "list-work",
        help="List all work packets with their current owner and step",
    )
    p_list_work.set_defaults(func=cmd_list_work)

    # new-agent
    p_new_agent = sub.add_parser(
        "new-agent",
        help="Scaffold a new agent stub under .agents/agents/<name>.toml",
    )
    p_new_agent.add_argument("name", metavar="<name>", help="Agent name (used as filename)")
    p_new_agent.set_defaults(func=cmd_new_agent)

    # new-skill
    p_new_skill = sub.add_parser(
        "new-skill",
        help="Scaffold a new skill stub under .agents/skills/<name>/SKILL.md",
    )
    p_new_skill.add_argument("name", metavar="<name>", help="Skill name (used as directory name)")
    p_new_skill.set_defaults(func=cmd_new_skill)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
