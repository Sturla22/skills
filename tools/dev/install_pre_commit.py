#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def git_output(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout.strip()


def resolve_repo_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path.resolve()
    return (REPO_ROOT / path).resolve()


def maybe_unset_default_hooks_path() -> None:
    hooks_path = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"],
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if hooks_path.returncode != 0:
        return

    configured_hooks_path = resolve_repo_path(hooks_path.stdout.strip())
    default_hooks_path = resolve_repo_path(git_output("rev-parse", "--git-path", "hooks"))
    if configured_hooks_path != default_hooks_path:
        raise SystemExit(
            "core.hooksPath is set to a non-default location. "
            "This repo will not overwrite a custom hook path; either install "
            "the pre-commit hook there manually or unset core.hooksPath first."
        )

    subprocess.run(
        ["git", "config", "--local", "--unset-all", "core.hooksPath"],
        cwd=REPO_ROOT,
        check=True,
    )


def main() -> int:
    maybe_unset_default_hooks_path()
    subprocess.run(
        [sys.executable, "-m", "pre_commit", "install"],
        cwd=REPO_ROOT,
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
