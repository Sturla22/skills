#!/usr/bin/env python3
from __future__ import annotations

import os
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BASE64_MIN_LENGTH = int(os.environ.get("DETECT_SECRETS_BASE64_MIN_LENGTH", "40"))
HEX_MIN_LENGTH = int(os.environ.get("DETECT_SECRETS_HEX_MIN_LENGTH", "40"))

SKIP_SUFFIXES = {".md", ".lock", ".sum"}
ALLOWLIST_TOKENS = ("# nosecret", "# pragma: allowlist secret")


def build_patterns() -> dict[str, re.Pattern[str]]:
    return {
        "aws_access_key_id": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "aws_secret_access_key": re.compile(
            r"(?i)\baws[_-]?secret[_-]?access[_-]?key\b\s*[=:]\s*['\"]?([A-Za-z0-9+/=]{40,})"
        ),
        "private_key_header": re.compile(
            r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
        ),
        "generic_api_key": re.compile(
            r"(?i)\b(?:api[_-]?key|api[_-]?secret|access[_-]?token|auth[_-]?token)\b\s*[=:]\s*['\"][^\s'\"]{8,}"
        ),
        "generic_password": re.compile(
            r"(?i)\b(?:password|passwd|pwd)\b\s*[=:]\s*['\"][^\s'\"]{8,}"
        ),
        "base64_secret": re.compile(rf"[A-Za-z0-9+/=]{{{BASE64_MIN_LENGTH},}}"),
        "hex_secret": re.compile(rf"[0-9a-fA-F]{{{HEX_MIN_LENGTH},}}"),
    }


def is_binary_file(file_path: Path) -> bool:
    try:
        with file_path.open("rb") as handle:
            return b"\x00" in handle.read(4096)
    except OSError:
        return False


def should_skip_path(file_path: Path) -> bool:
    return file_path.suffix.lower() in SKIP_SUFFIXES


def looks_like_placeholder_comment(line: str) -> bool:
    stripped = line.lstrip()
    if not stripped.startswith(("#", "//", ";", "/*")):
        return False
    return bool(
        re.search(r"\b(?:example|placeholder|sample|dummy|test|fake|mock|your)\b", stripped, re.I)
    )


def should_skip_line(line: str) -> bool:
    return any(token in line for token in ALLOWLIST_TOKENS) or looks_like_placeholder_comment(line)


def scan_file(file_path: Path, patterns: dict[str, re.Pattern[str]]) -> list[str]:
    findings: list[str] = []
    try:
        with file_path.open("r", encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, start=1):
                if should_skip_line(line):
                    continue
                for pattern_name, pattern in patterns.items():
                    if pattern.search(line):
                        findings.append(f"{file_path}:{line_number}:{pattern_name}")
    except OSError:
        return findings
    return findings


def filter_paths(argv_paths: list[str]) -> list[Path]:
    selected: list[Path] = []
    for raw_path in argv_paths:
        file_path = Path(raw_path).resolve()
        if not file_path.is_file():
            continue
        if should_skip_path(file_path):
            continue
        if is_binary_file(file_path):
            continue
        selected.append(file_path)
    return sorted(dict.fromkeys(selected))


def main() -> int:
    file_paths = filter_paths(sys.argv[1:])
    if not file_paths:
        return 0

    patterns = build_patterns()
    findings = [finding for path in file_paths for finding in scan_file(path, patterns)]
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
