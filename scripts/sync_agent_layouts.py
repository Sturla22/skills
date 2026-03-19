#!/usr/bin/env python3
"""Generate Claude, Copilot, and Codex agent files from canonical .agents sources."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_AGENTS = ROOT / ".agents" / "agents"
CANONICAL_SKILLS = ROOT / ".agents" / "skills"
CANONICAL_PROJECT = ROOT / ".agents" / "project" / "CLAUDE.md"

CLAUDE_AGENTS = ROOT / ".claude" / "agents"
CLAUDE_SKILLS = ROOT / ".claude" / "skills"
CLAUDE_PROJECT = ROOT / ".claude" / "CLAUDE.md"

COPILOT_AGENTS = ROOT / ".github" / "agents"
CODEX_AGENTS = ROOT / ".codex" / "agents"

CODEX_NOTE = "# GENERATED FILE. Edit the canonical source under .agents/ and run scripts/sync_agent_layouts.py\n"


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def read_toml(path: Path) -> dict:
    try:
        import tomllib  # type: ignore[import]
    except ImportError:
        import tomli as tomllib  # type: ignore[import,no-redef]
    with path.open("rb") as f:
        return tomllib.load(f)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str, check: bool, touched: list[Path], errors: list[str]) -> None:
    ensure_dir(path.parent)
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        touched.append(path)
        return
    if check:
        errors.append(str(path.relative_to(ROOT)))
        return
    path.write_text(content, encoding="utf-8")
    touched.append(path)


def format_yaml_list(values: list[str]) -> str:
    return "\n".join(f"  - {value}" for value in values) if values else "  []"


def generate_claude_agent(spec: dict) -> str:
    tools = spec.get("tools", [])
    skills = spec.get("skills", [])
    lines = [
        "---",
        f"name: {spec['name']}",
        f"description: {spec['description']}",
        f"tools: {', '.join(tools)}" if tools else "tools:",
        "model: inherit",
        "skills:",
        format_yaml_list(skills),
    ]
    if spec.get("claude_permission_mode"):
        lines.append(f"permissionMode: {spec['claude_permission_mode']}")
    if spec.get("claude_max_turns") is not None:
        lines.append(f"maxTurns: {spec['claude_max_turns']}")
    lines.append("---")
    return "\n".join(lines) + "\n" + spec["body"].rstrip() + "\n"


def generate_github_agent(spec: dict) -> str:
    body = spec.get("github_body") or spec["body"]
    return (
        "---\n"
        + f"name: {spec['name']}\n"
        + f"description: {spec['description']}\n"
        + "---\n"
        + body.rstrip()
        + "\n"
    )


def generate_codex_agent(spec: dict) -> str:
    nicknames = ", ".join(repr(n) for n in spec.get("codex_nickname_candidates", []))
    developer_instructions = spec["body"].rstrip()
    reasoning = spec.get("codex_model_reasoning_effort", "medium")
    sandbox = spec.get("codex_sandbox_mode", "workspace-write")
    return (
        CODEX_NOTE
        + f'name = "{spec["name"]}"\n'
        + f'description = "{spec["description"]}"\n'
        + f'model_reasoning_effort = "{reasoning}"\n'
        + f'sandbox_mode = "{sandbox}"\n'
        + f'nickname_candidates = [{nicknames}]\n'
        + 'developer_instructions = """\n'
        + developer_instructions
        + '\n"""\n'
    )


def copy_skills(check: bool, touched: list[Path], errors: list[str]) -> None:
    ensure_dir(CLAUDE_SKILLS)
    expected = set()
    for skill_dir in sorted(CANONICAL_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        src = skill_dir / "SKILL.md"
        if not src.exists():
            continue
        dst = CLAUDE_SKILLS / skill_dir.name / "SKILL.md"
        expected.add(str(dst.relative_to(CLAUDE_SKILLS)))
        write_file(dst, src.read_text(encoding="utf-8"), check, touched, errors)
    for existing in CLAUDE_SKILLS.rglob("SKILL.md"):
        rel = str(existing.relative_to(CLAUDE_SKILLS))
        if rel not in expected:
            if check:
                errors.append(str(existing.relative_to(ROOT)))
            else:
                existing.unlink()


def cleanup_files(folder: Path, wanted_names: set[str], suffix: str, check: bool, errors: list[str]) -> None:
    ensure_dir(folder)
    for child in folder.iterdir():
        if child.is_file() and child.name not in wanted_names and child.name.endswith(suffix):
            if check:
                errors.append(str(child.relative_to(ROOT)))
            else:
                child.unlink()


def link_skills_global() -> int:
    """Symlink each .claude/skills/<name> into ~/.claude/skills/<name>."""
    global_skills = Path.home() / ".claude" / "skills"
    global_skills.mkdir(parents=True, exist_ok=True)
    errors = 0
    for skill_dir in sorted(CLAUDE_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        target = global_skills / skill_dir.name
        if target.is_symlink():
            target.unlink()
        elif target.exists():
            print(f"skip: {skill_dir.name} (exists and is not a symlink)")
            errors += 1
            continue
        target.symlink_to(skill_dir.resolve())
        print(f"linked: {skill_dir.name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if generated files are out of date.")
    parser.add_argument("--link", action="store_true", help="Symlink .claude/skills/* into ~/.claude/skills/.")
    args = parser.parse_args()

    if args.link:
        return link_skills_global()


    touched: list[Path] = []
    errors: list[str] = []

    if CANONICAL_PROJECT.exists():
        write_file(CLAUDE_PROJECT, CANONICAL_PROJECT.read_text(encoding="utf-8"), args.check, touched, errors)

    expected_claude = set()
    expected_github = set()
    expected_codex = set()

    for spec_path in sorted(CANONICAL_AGENTS.glob("*.toml")):
        spec = read_toml(spec_path)
        for key in ("name", "description", "body"):
            if key not in spec:
                raise SystemExit(f"{spec_path} missing required field: {key}")

        expected_claude.add(f'{spec["name"]}.md')
        expected_github.add(f'{spec["name"]}.agent.md')
        expected_codex.add(f'{spec["name"]}.toml')

        write_file(CLAUDE_AGENTS / f'{spec["name"]}.md', generate_claude_agent(spec), args.check, touched, errors)
        write_file(COPILOT_AGENTS / f'{spec["name"]}.agent.md', generate_github_agent(spec), args.check, touched, errors)
        write_file(CODEX_AGENTS / f'{spec["name"]}.toml', generate_codex_agent(spec), args.check, touched, errors)

    cleanup_files(CLAUDE_AGENTS, expected_claude, ".md", args.check, errors)
    cleanup_files(COPILOT_AGENTS, expected_github, ".agent.md", args.check, errors)
    cleanup_files(CODEX_AGENTS, expected_codex, ".toml", args.check, errors)

    copy_skills(args.check, touched, errors)

    if errors:
        print("Generated files are out of date:")
        for item in sorted(set(errors)):
            print(f" - {item}")
        return 1

    mode = "Checked" if args.check else "Updated"
    fingerprint = stable_hash("\n".join(sorted(str(p.relative_to(ROOT)) for p in touched)))
    print(f"{mode} {len(touched)} generated files ({fingerprint}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
