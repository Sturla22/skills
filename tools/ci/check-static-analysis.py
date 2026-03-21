#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
STARTER_DIR = REPO_ROOT / "extras" / "cmake-nrf52840-template"
HOST_BUILD_DIR = STARTER_DIR / "build" / "host-debug"
TARGET_BUILD_DIR = STARTER_DIR / "build" / "nrf52840-debug"


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        raise SystemExit(f"Missing required tool: {name}")


def run_command(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def list_compile_db_files(compile_db_path: Path) -> list[Path]:
    entries = json.loads(compile_db_path.read_text())
    seen: set[str] = set()
    files: list[Path] = []
    for entry in entries:
        file_path = entry["file"]
        if file_path in seen:
            continue
        seen.add(file_path)
        files.append(Path(file_path))
    return files


def collect_cxx_include_dirs(compiler: str) -> list[str]:
    completed = subprocess.run(
        [compiler, "-xc++", "-E", "-v", "/dev/null"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    lines = completed.stdout.splitlines()
    start_marker = "#include <...> search starts here:"
    end_marker = "End of search list."
    try:
        start_index = lines.index(start_marker) + 1
        end_index = lines.index(end_marker)
    except ValueError as exc:
        raise SystemExit(
            f"Failed to discover standard include paths from {compiler}."
        ) from exc
    return [line.strip() for line in lines[start_index:end_index] if line.strip()]


def build_clang_tidy_extra_args(
    compiler: str, *, target_triple: str | None = None
) -> list[str]:
    extra_args: list[str] = []
    if target_triple is not None:
        extra_args.append(f"--extra-arg=--target={target_triple}")
    for include_dir in collect_cxx_include_dirs(compiler):
        extra_args.append(f"--extra-arg=-isystem{include_dir}")
    return extra_args


def classify_host_files(files: list[Path]) -> list[Path]:
    return [
        file_path
        for file_path in files
        if "libs/domain/" in file_path.as_posix() or "tests/host/" in file_path.as_posix()
    ]


def classify_target_files(files: list[Path]) -> list[Path]:
    return [
        file_path
        for file_path in files
        if "libs/platform/" in file_path.as_posix() or "/src/" in file_path.as_posix()
    ]


def run_clang_tidy(files: list[Path], build_dir: Path, extra_args: list[str]) -> None:
    for file_path in files:
        run_command("clang-tidy", str(file_path), "-p", str(build_dir), *extra_args)


def main() -> int:
    for tool in ("cmake", "clang-tidy", "c++", "arm-none-eabi-g++"):
        require_tool(tool)

    run_command("cmake", "--preset", "host-debug", "--fresh", cwd=STARTER_DIR)
    run_command("cmake", "--preset", "nrf52840-debug", "--fresh", cwd=STARTER_DIR)

    host_candidates = list_compile_db_files(HOST_BUILD_DIR / "compile_commands.json")
    target_candidates = list_compile_db_files(TARGET_BUILD_DIR / "compile_commands.json")

    host_files = classify_host_files(host_candidates)
    target_files = classify_target_files(target_candidates)

    host_extra_args = build_clang_tidy_extra_args("c++")
    target_extra_args = build_clang_tidy_extra_args(
        "arm-none-eabi-g++", target_triple="arm-none-eabi"
    )

    run_clang_tidy(host_files, HOST_BUILD_DIR, host_extra_args)
    run_clang_tidy(target_files, TARGET_BUILD_DIR, target_extra_args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
