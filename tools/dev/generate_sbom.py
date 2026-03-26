#!/usr/bin/env python3
from __future__ import annotations

import argparse
import configparser
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def external_dir_has_contents(external_dir: Path) -> bool:
    return external_dir.exists() and any(external_dir.iterdir())


def read_text_if_exists(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8", errors="replace")


def version_from_version_file(component_dir: Path) -> str | None:
    for version_file in sorted(component_dir.rglob("VERSION")):
        contents = read_text_if_exists(version_file)
        if contents is None:
            continue
        for line in contents.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped
    return None


def version_from_cmake(component_dir: Path) -> str | None:
    pattern = re.compile(r"project\s*\(.*?\bVERSION\s+([^\s)]+)", re.IGNORECASE | re.DOTALL)
    for cmake_file in sorted(component_dir.rglob("CMakeLists.txt")):
        contents = read_text_if_exists(cmake_file)
        if contents is None:
            continue
        match = pattern.search(contents)
        if match is not None:
            return match.group(1)
    return None


def version_from_package_json(component_dir: Path) -> str | None:
    for package_json in sorted(component_dir.rglob("package.json")):
        contents = read_text_if_exists(package_json)
        if contents is None:
            continue
        try:
            data = json.loads(contents)
        except json.JSONDecodeError:
            continue
        version = data.get("version")
        if isinstance(version, str) and version.strip():
            return version.strip()
    return None


def parse_gitmodules() -> dict[str, str]:
    gitmodules_path = REPO_ROOT / ".gitmodules"
    if not gitmodules_path.is_file():
        return {}

    parser = configparser.ConfigParser(interpolation=None)
    parser.read(gitmodules_path, encoding="utf-8")

    submodules: dict[str, str] = {}
    for section in parser.sections():
        path = parser.get(section, "path", fallback="").strip()
        branch = parser.get(section, "branch", fallback="").strip()
        if path:
            submodules[path] = branch
    return submodules


def version_from_gitmodules(component_dir: Path) -> str | None:
    submodules = parse_gitmodules()
    if not submodules:
        return None

    relative_path = component_dir.relative_to(REPO_ROOT).as_posix()
    branch = submodules.get(relative_path)
    if branch:
        return branch

    return None


def detect_component_version(component_dir: Path) -> str:
    for detector in (
        version_from_version_file,
        version_from_cmake,
        version_from_package_json,
        version_from_gitmodules,
    ):
        version = detector(component_dir)
        if version:
            return version
    return "unknown"


def collect_components(external_dir: Path) -> list[dict[str, str]]:
    if not external_dir_has_contents(external_dir):
        return []

    components: list[dict[str, str]] = []
    for component_dir in sorted(path for path in external_dir.iterdir() if path.is_dir()):
        components.append(
            {
                "type": "library",
                "name": component_dir.name,
                "version": detect_component_version(component_dir),
            }
        )
    return components


def build_sbom(external_dir: Path) -> dict[str, object]:
    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "components": collect_components(external_dir),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a minimal CycloneDX SBOM for external dependencies.")
    parser.add_argument("--output", type=Path, help="Write the SBOM JSON to a file instead of stdout.")
    return parser.parse_args(argv)


def emit_sbom(sbom: dict[str, object], output_path: Path | None) -> None:
    serialized = json.dumps(sbom, indent=2, sort_keys=True)
    if output_path is None:
        print(serialized)
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(serialized + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    external_dir = REPO_ROOT / "external"
    emit_sbom(build_sbom(external_dir), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
