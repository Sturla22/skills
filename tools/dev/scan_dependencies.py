#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def external_dir_has_contents(external_dir: Path) -> bool:
    return external_dir.exists() and any(external_dir.iterdir())


def run_scanner(scanner_name: str, command: list[str]) -> int:
    print(f"Using {scanner_name}.")
    completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
    return completed.returncode


def main() -> int:
    external_dir = REPO_ROOT / "external"
    if not external_dir_has_contents(external_dir):
        print("No external dependencies found.")
        return 0

    osv_scanner = shutil.which("osv-scanner")
    if osv_scanner is not None:
        return run_scanner("osv-scanner", [osv_scanner, "--recursive", str(external_dir)])

    trivy = shutil.which("trivy")
    if trivy is not None:
        return run_scanner("trivy", [trivy, "fs", str(external_dir)])

    print(
        "No dependency scanner found. Install one of: osv-scanner "
        "(https://github.com/google/osv-scanner), trivy (https://trivy.dev). "
        "Skipping scan."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
