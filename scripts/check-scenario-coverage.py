#!/usr/bin/env python3
"""Check that every SC-NNN scenario in docs/scenarios.md and
docs/work/*/scenarios.md is covered by at least one test file containing
a 'Covers: SC-NNN' comment. Reports uncovered scenarios and orphaned
test references. Exits 1 if any gap or orphan is found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Matches SC-NNN IDs (three or more digits, zero-padded by convention).
ID_PATTERN = re.compile(r"\bSC-\d+\b")


def collect_scenario_ids(root: Path) -> dict[str, list[str]]:
    """Return {sc_id: [file_path, ...]} from all scenario files under root."""
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
        for match in ID_PATTERN.finditer(sf.read_text(encoding="utf-8")):
            sc_id = match.group()
            ids.setdefault(sc_id, []).append(rel)
    return ids


def collect_covered_ids(root: Path, tests_glob: str) -> dict[str, list[str]]:
    """Return {sc_id: [file_path, ...]} from Covers: comments in test files."""
    covered: dict[str, list[str]] = {}
    for test_file in sorted(root.glob(tests_glob)):
        if not test_file.is_file():
            continue
        try:
            text = test_file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(test_file.relative_to(root))
        for match in ID_PATTERN.finditer(text):
            # Only count occurrences that are prefixed by 'Covers:' on the same line.
            line_start = text.rfind("\n", 0, match.start()) + 1
            line_end = text.find("\n", match.end())
            line = text[line_start:] if line_end == -1 else text[line_start:line_end]
            if "Covers:" in line:
                sc_id = match.group()
                covered.setdefault(sc_id, []).append(rel)
    return covered


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify SC-NNN scenario coverage across test files."
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repo root to resolve paths from (default: current directory).",
    )
    parser.add_argument(
        "--tests",
        default="tests/**/*",
        help="Glob for test files relative to root (default: tests/**/*).",
    )
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    scenario_ids = collect_scenario_ids(root)
    covered_ids = collect_covered_ids(root, args.tests)

    scenario_file_count = len(
        ([root / "docs" / "scenarios.md"] if (root / "docs" / "scenarios.md").exists() else [])
        + list((root / "docs" / "work").glob("*/scenarios.md") if (root / "docs" / "work").exists() else [])
    )
    # Count distinct test files touched.
    test_files_seen: set[str] = set()
    for paths in covered_ids.values():
        test_files_seen.update(paths)

    print(f"Scanning {scenario_file_count} scenario file(s), "
          f"{len(test_files_seen)} test file(s) with coverage references...\n")

    uncovered = [sc_id for sc_id in sorted(scenario_ids) if sc_id not in covered_ids]
    orphaned = [sc_id for sc_id in sorted(covered_ids) if sc_id not in scenario_ids]

    if uncovered:
        print("UNCOVERED SCENARIOS:")
        for sc_id in uncovered:
            files = ", ".join(scenario_ids[sc_id])
            print(f"  {sc_id}  [{files}]")
        print()

    if orphaned:
        print("ORPHANED REFERENCES (in tests but not defined in any scenarios file):")
        for sc_id in orphaned:
            files = ", ".join(covered_ids[sc_id])
            print(f"  {sc_id}  {files}")
        print()

    total = len(scenario_ids)
    n_covered = total - len(uncovered)
    status = "OK" if not uncovered and not orphaned else "FAIL"
    print(f"Result: {n_covered}/{total} covered, "
          f"{len(uncovered)} uncovered, "
          f"{len(orphaned)} orphaned — {status}")

    return 0 if status == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
