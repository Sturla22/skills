#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
STARTER_DIR = REPO_ROOT / "extras" / "cmake-nrf52840-template"
SOURCE_ROOTS = (
    STARTER_DIR / "libs",
    STARTER_DIR / "src",
    STARTER_DIR / "tests",
)
SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".cxx", ".h", ".hpp"}


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Missing required tool: {name}")


def iter_starter_source_files() -> list[Path]:
    return sorted(
        file_path
        for source_root in SOURCE_ROOTS
        for file_path in source_root.rglob("*")
        if file_path.is_file() and file_path.suffix in SOURCE_SUFFIXES
    )


def main() -> int:
    require_tool("clang-format")
    file_paths = iter_starter_source_files()
    if not file_paths:
        return 0

    subprocess.run(
        [
            "clang-format",
            "--dry-run",
            "--Werror",
            "--style=file",
            *(str(path) for path in file_paths),
        ],
        cwd=REPO_ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
