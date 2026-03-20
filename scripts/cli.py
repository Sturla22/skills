#!/usr/bin/env python3
"""scripts/cli.py — scaffolding and inspection CLI for this repo.

All subcommands exit 0 on success, non-zero on error.
No ANSI colour codes. No interactive prompts. No pip dependencies.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import os
import re
import shutil
import subprocess
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
    "Reminder: run `python scripts/cli.py sync` "
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


def _run_command(command: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError as exc:
        return 127, str(exc)

    output = (proc.stdout or "").strip()
    if not output:
        output = (proc.stderr or "").strip()
    return proc.returncode, output


def _print_check(status: str, label: str, detail: str | None = None) -> None:
    line = f"[{status}] {label}"
    if detail:
        line += f": {detail}"
    print(line)


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
# Sync helpers
# ---------------------------------------------------------------------------

CANONICAL_AGENTS = ROOT / ".agents" / "agents"
CANONICAL_SKILLS = ROOT / ".agents" / "skills"
CANONICAL_RULES  = ROOT / ".agents" / "rules"
CANONICAL_PROJECT = ROOT / ".agents" / "project" / "CLAUDE.md"

CLAUDE_AGENTS  = ROOT / ".claude" / "agents"
CLAUDE_SKILLS  = ROOT / ".claude" / "skills"
CLAUDE_RULES   = ROOT / ".claude" / "rules"
CLAUDE_PROJECT = ROOT / ".claude" / "CLAUDE.md"

COPILOT_AGENTS = ROOT / ".github" / "agents"
CODEX_AGENTS   = ROOT / ".codex"  / "agents"

CODEX_NOTE = (
    "# GENERATED FILE. Edit the canonical source under .agents/ "
    "and run scripts/cli.py sync\n"
)


def _stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def _read_toml(path: Path) -> dict:
    try:
        import tomllib          # type: ignore[import]
    except ImportError:
        import tomli as tomllib  # type: ignore[import,no-redef]
    with path.open("rb") as f:
        return tomllib.load(f)


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _sync_write_file(
    path: Path, content: str, check: bool,
    touched: list[Path], errors: list[str],
) -> None:
    _ensure_dir(path.parent)
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        touched.append(path)
        return
    if check:
        errors.append(str(path.relative_to(ROOT)))
        return
    path.write_text(content, encoding="utf-8")
    touched.append(path)


def _format_yaml_list(values: list[str]) -> str:
    return "\n".join(f"  - {value}" for value in values) if values else "  []"


def _generate_claude_agent(spec: dict) -> str:
    tools  = spec.get("tools", [])
    skills = spec.get("skills", [])
    claude_model = spec.get("claude_model", "inherit")
    lines = [
        "---",
        f"name: {spec['name']}",
        f"description: {spec['description']}",
        f"tools: {', '.join(tools)}" if tools else "tools:",
        f"model: {claude_model}",
        "skills:",
        _format_yaml_list(skills),
    ]
    if spec.get("claude_permission_mode"):
        lines.append(f"permissionMode: {spec['claude_permission_mode']}")
    if spec.get("claude_max_turns") is not None:
        lines.append(f"maxTurns: {spec['claude_max_turns']}")
    lines.append("---")
    return "\n".join(lines) + "\n" + spec["body"].rstrip() + "\n"


def _generate_github_agent(spec: dict) -> str:
    body = spec.get("github_body") or spec["body"]
    return (
        "---\n"
        + f"name: {spec['name']}\n"
        + f"description: {spec['description']}\n"
        + "---\n"
        + body.rstrip()
        + "\n"
    )


def _generate_codex_agent(spec: dict) -> str:
    nicknames = ", ".join(repr(n) for n in spec.get("codex_nickname_candidates", []))
    reasoning = spec.get("codex_model_reasoning_effort", "medium")
    sandbox   = spec.get("codex_sandbox_mode", "workspace-write")
    return (
        CODEX_NOTE
        + f'name = "{spec["name"]}"\n'
        + f'description = "{spec["description"]}"\n'
        + f'model_reasoning_effort = "{reasoning}"\n'
        + f'sandbox_mode = "{sandbox}"\n'
        + f'nickname_candidates = [{nicknames}]\n'
        + 'developer_instructions = """\n'
        + spec["body"].rstrip()
        + '\n"""\n'
    )


def _copy_skills(check: bool, touched: list[Path], errors: list[str]) -> None:
    _ensure_dir(CLAUDE_SKILLS)
    expected: set[str] = set()
    for skill_dir in sorted(CANONICAL_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        src = skill_dir / "SKILL.md"
        if not src.exists():
            continue
        dst = CLAUDE_SKILLS / skill_dir.name / "SKILL.md"
        expected.add(str(dst.relative_to(CLAUDE_SKILLS)))
        _sync_write_file(dst, src.read_text(encoding="utf-8"), check, touched, errors)
    for existing in CLAUDE_SKILLS.rglob("SKILL.md"):
        rel = str(existing.relative_to(CLAUDE_SKILLS))
        if rel not in expected:
            if check:
                errors.append(str(existing.relative_to(ROOT)))
            else:
                existing.unlink()


def _copy_rules(check: bool, touched: list[Path], errors: list[str]) -> None:
    if not CANONICAL_RULES.exists():
        return
    _ensure_dir(CLAUDE_RULES)
    expected: set[str] = set()
    for src in sorted(CANONICAL_RULES.glob("*.md")):
        dst = CLAUDE_RULES / src.name
        expected.add(src.name)
        _sync_write_file(dst, src.read_text(encoding="utf-8"), check, touched, errors)
    for existing in CLAUDE_RULES.glob("*.md"):
        if existing.name not in expected:
            if check:
                errors.append(str(existing.relative_to(ROOT)))
            else:
                existing.unlink()


def _cleanup_files(
    folder: Path, wanted_names: set[str], suffix: str,
    check: bool, errors: list[str],
) -> None:
    _ensure_dir(folder)
    for child in folder.iterdir():
        if child.is_file() and child.name not in wanted_names and child.name.endswith(suffix):
            if check:
                errors.append(str(child.relative_to(ROOT)))
            else:
                child.unlink()


def _link_skills_global() -> int:
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


# ---------------------------------------------------------------------------
# Subcommand: sync
# ---------------------------------------------------------------------------

def cmd_sync(args: argparse.Namespace) -> None:
    if args.link:
        sys.exit(_link_skills_global())

    touched: list[Path] = []
    errors:  list[str]  = []

    if CANONICAL_PROJECT.exists():
        _sync_write_file(
            CLAUDE_PROJECT,
            CANONICAL_PROJECT.read_text(encoding="utf-8"),
            args.check, touched, errors,
        )

    expected_claude: set[str] = set()
    expected_github: set[str] = set()
    expected_codex:  set[str] = set()

    for spec_path in sorted(CANONICAL_AGENTS.glob("*.toml")):
        spec = _read_toml(spec_path)
        for key in ("name", "description", "body"):
            if key not in spec:
                raise SystemExit(f"{spec_path} missing required field: {key}")

        expected_claude.add(f'{spec["name"]}.md')
        expected_github.add(f'{spec["name"]}.agent.md')
        expected_codex.add(f'{spec["name"]}.toml')

        _sync_write_file(CLAUDE_AGENTS  / f'{spec["name"]}.md',        _generate_claude_agent(spec),  args.check, touched, errors)
        _sync_write_file(COPILOT_AGENTS / f'{spec["name"]}.agent.md',  _generate_github_agent(spec),  args.check, touched, errors)
        _sync_write_file(CODEX_AGENTS   / f'{spec["name"]}.toml',      _generate_codex_agent(spec),   args.check, touched, errors)

    _cleanup_files(CLAUDE_AGENTS,  expected_claude, ".md",       args.check, errors)
    _cleanup_files(COPILOT_AGENTS, expected_github, ".agent.md", args.check, errors)
    _cleanup_files(CODEX_AGENTS,   expected_codex,  ".toml",     args.check, errors)

    _copy_skills(args.check, touched, errors)
    _copy_rules(args.check, touched, errors)

    if errors:
        print("Generated files are out of date:")
        for item in sorted(set(errors)):
            print(f" - {item}")
        sys.exit(1)

    mode = "Checked" if args.check else "Updated"
    fingerprint = _stable_hash("\n".join(sorted(str(p.relative_to(ROOT)) for p in touched)))
    print(f"{mode} {len(touched)} generated files ({fingerprint}).")


# ---------------------------------------------------------------------------
# Coverage helpers
# ---------------------------------------------------------------------------

_SC_ID_PATTERN = re.compile(r"\bSC-\d+\b")


def _collect_scenario_ids(root: Path) -> dict[str, list[str]]:
    scenario_files: list[Path] = []
    project_level = root / "docs" / "scenarios.md"
    if project_level.exists():
        scenario_files.append(project_level)
    work_dir = root / "docs" / "work"
    if work_dir.is_dir():
        for wp_file in sorted(work_dir.glob("*/scenarios.md")):
            scenario_files.append(wp_file)
    ids: dict[str, list[str]] = {}
    for sf in scenario_files:
        rel = str(sf.relative_to(root))
        for match in _SC_ID_PATTERN.finditer(sf.read_text(encoding="utf-8")):
            ids.setdefault(match.group(), []).append(rel)
    return ids


def _collect_covered_ids(root: Path, tests_glob: str) -> dict[str, list[str]]:
    covered: dict[str, list[str]] = {}
    for test_file in sorted(root.glob(tests_glob)):
        if not test_file.is_file():
            continue
        try:
            text = test_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(test_file.relative_to(root))
        for match in _SC_ID_PATTERN.finditer(text):
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end   = text.find("\n", match.end())
            line = text[line_start:] if line_end == -1 else text[line_start:line_end]
            if "Covers:" in line:
                covered.setdefault(match.group(), []).append(rel)
    return covered


# ---------------------------------------------------------------------------
# Subcommand: check-coverage
# ---------------------------------------------------------------------------

def cmd_check_coverage(args: argparse.Namespace) -> None:
    root = Path(args.root).resolve() if args.root else ROOT
    tests_glob = args.tests or "tests/**/*"

    scenario_ids = _collect_scenario_ids(root)
    covered_ids  = _collect_covered_ids(root, tests_glob)

    sf_count = len(
        ([root / "docs" / "scenarios.md"] if (root / "docs" / "scenarios.md").exists() else [])
        + list((root / "docs" / "work").glob("*/scenarios.md")
               if (root / "docs" / "work").exists() else [])
    )
    test_files_seen: set[str] = set()
    for paths in covered_ids.values():
        test_files_seen.update(paths)

    print(f"Scanning {sf_count} scenario file(s), "
          f"{len(test_files_seen)} test file(s) with coverage references...\n")

    uncovered = [sc for sc in sorted(scenario_ids) if sc not in covered_ids]
    orphaned  = [sc for sc in sorted(covered_ids)  if sc not in scenario_ids]

    if uncovered:
        print("UNCOVERED SCENARIOS:")
        for sc in uncovered:
            print(f"  {sc}  [{', '.join(scenario_ids[sc])}]")
        print()
    if orphaned:
        print("ORPHANED REFERENCES (in tests but not defined in any scenarios file):")
        for sc in orphaned:
            print(f"  {sc}  {', '.join(covered_ids[sc])}")
        print()

    total   = len(scenario_ids)
    n_cov   = total - len(uncovered)
    status  = "OK" if not uncovered and not orphaned else "FAIL"
    print(f"Result: {n_cov}/{total} covered, "
          f"{len(uncovered)} uncovered, "
          f"{len(orphaned)} orphaned — {status}")
    sys.exit(0 if status == "OK" else 1)


# ---------------------------------------------------------------------------
# Subcommand: doctor
# ---------------------------------------------------------------------------

def _check_path_exists(path: Path, label: str) -> tuple[bool, str]:
    if path.exists():
        return True, label
    return False, f"missing: {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}"


def _doctor_check_binary(name: str) -> tuple[str, str]:
    resolved = shutil.which(name)
    if not resolved:
        return "FAIL", "not installed or not on PATH"
    return "OK", resolved


def _doctor_check_auth(tool: str) -> tuple[str, str]:
    if tool == "codex":
        code, output = _run_command(["codex", "login", "status"])
    elif tool == "claude":
        code, output = _run_command(["claude", "auth", "status"])
    else:
        return "WARN", "no auth check implemented"

    if code == 0:
        if output.startswith("{"):
            try:
                payload = json.loads(output)
            except json.JSONDecodeError:
                pass
            else:
                if payload.get("loggedIn") is True:
                    auth_method = payload.get("authMethod", "unknown")
                    return "OK", f"authenticated via {auth_method}"
        return "OK", output.splitlines()[0] if output else "authenticated"
    return "WARN", output.splitlines()[0] if output else "authentication not confirmed"


def _doctor_optional_repo_surface(path: Path, label: str) -> tuple[str, str | None]:
    if path.exists():
        return "OK", None
    return "WARN", f"not installed yet: {label}"


def cmd_doctor(args: argparse.Namespace) -> None:
    tool = args.tool
    mode = args.mode
    failures = 0
    warnings = 0

    print(f"Doctor for {tool} ({mode}) in {ROOT}")
    print()

    status, detail = _doctor_check_binary("python3")
    _print_check(status, "python3", detail)
    if status != "OK":
        failures += 1

    if mode == "existing":
        required_paths = [
            ROOT / ".git",
        ]
    else:
        required_paths = [
            ROOT / "README.md",
            ROOT / "AGENTS.md",
            ROOT / ".agents",
            ROOT / "scripts" / "cli.py",
        ]
    for path in required_paths:
        ok, detail = _check_path_exists(path, path.name)
        if ok:
            _print_check("OK", f"repo file {path.relative_to(ROOT)}")
        else:
            _print_check("FAIL", f"repo file {path.name}", detail)
            failures += 1

    if mode == "existing":
        canonical_layer = ROOT / ".agents"
        if canonical_layer.exists():
            code, output = _run_command(["python3", "scripts/cli.py", "sync", "--check"])
            if code == 0:
                _print_check("OK", "generated files in sync", output)
            else:
                _print_check("FAIL", "generated files in sync", output)
                failures += 1
        else:
            _print_check(
                "WARN",
                "starter repo surfaces",
                "canonical .agents layer not installed yet; copy the minimum adoption slice before rerunning sync checks",
            )
            warnings += 1
    else:
        code, output = _run_command(["python3", "scripts/cli.py", "sync", "--check"])
        if code == 0:
            _print_check("OK", "generated files in sync", output)
        else:
            _print_check("FAIL", "generated files in sync", output)
            failures += 1

    if tool in ("codex", "all"):
        status, detail = _doctor_check_binary("codex")
        _print_check(status, "codex CLI", detail)
        if status != "OK":
            failures += 1
        else:
            status, detail = _doctor_check_auth("codex")
            _print_check(status, "codex auth", detail)
            if status == "WARN":
                warnings += 1

        config_path = ROOT / ".codex" / "config.toml"
        if mode == "existing":
            status, detail = _doctor_optional_repo_surface(config_path, ".codex/config.toml")
            _print_check(status, "Codex config", detail)
            if status == "WARN":
                warnings += 1
        else:
            ok, detail = _check_path_exists(config_path, ".codex/config.toml")
            _print_check("OK" if ok else "FAIL", "Codex config", detail if not ok else None)
            if not ok:
                failures += 1

    if tool in ("claude", "all"):
        status, detail = _doctor_check_binary("claude")
        _print_check(status, "claude CLI", detail)
        if status != "OK":
            failures += 1
        else:
            status, detail = _doctor_check_auth("claude")
            _print_check(status, "claude auth", detail)
            if status == "WARN":
                warnings += 1

        settings_path = ROOT / ".claude" / "settings.json"
        if mode == "existing":
            status, detail = _doctor_optional_repo_surface(settings_path, ".claude/settings.json")
            _print_check(status, "Claude settings", detail)
            if status == "WARN":
                warnings += 1
        else:
            ok, detail = _check_path_exists(settings_path, ".claude/settings.json")
            _print_check("OK" if ok else "FAIL", "Claude settings", detail if not ok else None)
            if not ok:
                failures += 1

    if tool in ("copilot", "all"):
        copilot_paths = [
            ROOT / ".github" / "copilot-instructions.md",
            ROOT / ".github" / "agents",
            ROOT / ".vscode" / "settings.json",
        ]
        for path in copilot_paths:
            if mode == "existing":
                status, detail = _doctor_optional_repo_surface(path, str(path.relative_to(ROOT)))
                _print_check(status, f"Copilot repo surface {path.relative_to(ROOT)}", detail)
                if status == "WARN":
                    warnings += 1
            else:
                ok, detail = _check_path_exists(path, str(path.relative_to(ROOT)))
                _print_check("OK" if ok else "FAIL", f"Copilot repo surface {path.relative_to(ROOT)}", detail if not ok else None)
                if not ok:
                    failures += 1
        _print_check("WARN", "Copilot auth", "validate sign-in from your IDE or GitHub UI")
        warnings += 1

    print()
    if failures:
        print(f"Doctor result: FAIL ({failures} failing check(s), {warnings} warning(s))")
        sys.exit(1)

    print(f"Doctor result: OK ({warnings} warning(s))")


# ---------------------------------------------------------------------------
# Subcommand: first-run
# ---------------------------------------------------------------------------

def _first_run_lines(tool: str, mode: str) -> list[str]:
    if mode == "existing":
        common = [
            "1. Validate the repo surface:",
            "   `python3 scripts/cli.py doctor --tool {tool} --mode existing`",
            "2. Decide the minimum adoption slice:",
            "   Start with instructions only, generated agents, or work packets for non-trivial tasks. Do not replace existing repo conventions wholesale.",
            "3. Inventory conventions you must preserve:",
            "   Issue tracker IDs, commit and PR title rules, release process, CI checks, docs layout, test commands, and any existing agent or instruction files.",
            "4. Decide commit and PR naming policy:",
            "   Ask whether Jira ticket IDs should prefix commit messages and pull request titles.",
            "5. Copy the minimum starter surfaces you chose into the existing repo.",
            "   Examples: `AGENTS.md`, `.agents/project/CLAUDE.md`, `.github/copilot-instructions.md`, `.agents/agents/*.toml`, or work-packet templates.",
            "6. If you installed the canonical `.agents` layer, regenerate and verify derived files:",
            "   `python3 scripts/cli.py sync`",
            "   `python3 scripts/cli.py sync --check`",
            "7. Scaffold a pilot work packet for one real task when you are ready to trial the workflow:",
            "   `python3 scripts/cli.py new-work adoption-pilot`",
            "8. Record the conventions to preserve in `docs/work/adoption-pilot/brief.md`, then verify it:",
            "   `python3 scripts/cli.py check-work adoption-pilot`",
        ]
        prompts = {
            "codex": '9. Start Codex in the existing repo and use this first prompt:\n   `codex "Use product-owner to adapt this roles-and-skills workflow into an existing repository. First identify the conventions we must preserve, ask whether Jira ticket IDs should prefix commit messages and PR titles, then propose the smallest adoption slice and the first durable artifact to create."`',
            "claude": '9. Start Claude in the existing repo and use this first prompt:\n   `claude --permission-mode plan -p "Use product-owner to adapt this roles-and-skills workflow into an existing repository. First identify the conventions we must preserve, ask whether Jira ticket IDs should prefix commit messages and PR titles, then propose the smallest adoption slice and the first durable artifact to create."`',
            "copilot": '9. In your IDE chat, use this first prompt:\n   `Use product-owner to adapt this roles-and-skills workflow into an existing repository. First identify the conventions we must preserve, ask whether Jira ticket IDs should prefix commit messages and PR titles, then propose the smallest adoption slice and the first durable artifact to create.`',
        }
    else:
        common = [
            "1. Validate the repo surface:",
            "   `python3 scripts/cli.py doctor --tool {tool}`",
            "2. Regenerate and verify derived files:",
            "   `python3 scripts/cli.py sync`",
            "   `python3 scripts/cli.py sync --check`",
            "3. Decide commit and PR naming policy:",
            "   Ask whether Jira ticket IDs should prefix commit messages and pull request titles.",
            "4. Scaffold a first work packet:",
            "   `python3 scripts/cli.py new-work onboarding-demo`",
            "5. Fill `docs/work/onboarding-demo/brief.md`, then verify it:",
            "   `python3 scripts/cli.py check-work onboarding-demo`",
        ]
        prompts = {
            "codex": '6. Start Codex in the repo root and use this first prompt:\n   `codex "Use product-owner to summarize the current instructions and available skills, ask whether Jira ticket IDs should prefix commit messages and PR titles, then tell me the next owner and the first durable artifact to create."`',
            "claude": '6. Start Claude in the repo root and use this first prompt:\n   `claude --permission-mode plan -p "Use product-owner to summarize the current instructions and available skills, ask whether Jira ticket IDs should prefix commit messages and PR titles, then tell me the next owner and the first durable artifact to create."`',
            "copilot": '6. In your IDE chat, use this first prompt:\n   `Use product-owner to summarize the current instructions and available skills, ask whether Jira ticket IDs should prefix commit messages and PR titles, then tell me the next owner and the first durable artifact to create.`',
        }

    rendered = [line.format(tool=tool) for line in common]
    rendered.append(prompts[tool])
    return rendered


def cmd_first_run(args: argparse.Namespace) -> None:
    tool = args.tool
    mode = args.mode
    print(f"First-run guide for {tool} ({mode})")
    print()
    for line in _first_run_lines(tool, mode):
        print(line)


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

    # sync
    p_sync = sub.add_parser(
        "sync",
        help="Sync canonical .agents/ sources to .claude/, .github/, and .codex/",
    )
    p_sync.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if generated files are out of date (dry-run)",
    )
    p_sync.add_argument(
        "--link",
        action="store_true",
        help="Symlink .claude/skills/* into ~/.claude/skills/ instead of syncing",
    )
    p_sync.set_defaults(func=cmd_sync)

    # check-coverage
    p_check_coverage = sub.add_parser(
        "check-coverage",
        help="Check that every SC-NNN scenario is covered by at least one test",
    )
    p_check_coverage.add_argument(
        "--root",
        metavar="<dir>",
        default=None,
        help="Repo root to resolve paths from (default: repo root of this script)",
    )
    p_check_coverage.add_argument(
        "--tests",
        metavar="<glob>",
        default=None,
        help="Glob for test files relative to root (default: tests/**/*)",
    )
    p_check_coverage.set_defaults(func=cmd_check_coverage)

    # doctor
    p_doctor = sub.add_parser(
        "doctor",
        help="Check whether the local setup is ready for adoption",
    )
    p_doctor.add_argument(
        "--tool",
        choices=("all", "codex", "claude", "copilot"),
        default="all",
        help="Tooling surface to validate (default: all)",
    )
    p_doctor.add_argument(
        "--mode",
        choices=("starter", "existing"),
        default="starter",
        help="Validation mode (default: starter)",
    )
    p_doctor.set_defaults(func=cmd_doctor)

    # first-run
    p_first_run = sub.add_parser(
        "first-run",
        help="Print the recommended first-run sequence for a tool",
    )
    p_first_run.add_argument(
        "--tool",
        choices=("codex", "claude", "copilot"),
        required=True,
        help="Tooling surface to guide",
    )
    p_first_run.add_argument(
        "--mode",
        choices=("starter", "existing"),
        default="starter",
        help="Onboarding mode to guide (default: starter)",
    )
    p_first_run.set_defaults(func=cmd_first_run)

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
