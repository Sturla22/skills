#!/usr/bin/env python3
"""Start GitHub Copilot CLI with the product-owner custom agent selected."""

from __future__ import annotations

import shutil
import subprocess
import sys


DEFAULT_AGENT = "product-owner"


def build_copilot_command(argv: list[str]) -> list[str]:
    for index, arg in enumerate(argv):
        if arg == "--agent":
            raise ValueError(
                "Do not pass --agent to this launcher; it always starts Copilot "
                f"with {DEFAULT_AGENT!r}."
            )
        if arg.startswith("--agent="):
            raise ValueError(
                "Do not pass --agent to this launcher; it always starts Copilot "
                f"with {DEFAULT_AGENT!r}."
            )
        if arg == "-" and index == 0:
            break

    return ["copilot", "--agent", DEFAULT_AGENT, *argv]


def main(argv: list[str] | None = None) -> int:
    effective_argv = list(sys.argv[1:] if argv is None else argv)

    try:
        command = build_copilot_command(effective_argv)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if shutil.which("copilot") is None:
        print(
            "ERROR: 'copilot' was not found on PATH. Install GitHub Copilot CLI "
            "and ensure the executable is available before using this launcher.",
            file=sys.stderr,
        )
        return 127

    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
