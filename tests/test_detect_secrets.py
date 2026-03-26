import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "tools" / "dev" / "detect_secrets.py"
SCRIPT_SPEC = importlib.util.spec_from_file_location("detect_secrets", SCRIPT_PATH)
assert SCRIPT_SPEC is not None
assert SCRIPT_SPEC.loader is not None
detect_secrets = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(detect_secrets)


def test_main_reports_common_secret_patterns(tmp_path, monkeypatch, capsys):
    secret_file = tmp_path / "secrets.txt"
    secret_file.write_text(
        "\n".join(
            [
                "api_key = 'abcdEFGH1234ijklMNOP5678qrstUVWX'",
                "password: 'hunter2-hunter2'",
                "aws_secret_access_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcd'",
                "token = '0123456789abcdef0123456789abcdef01234567'",
                "0123456789abcdef0123456789abcdef01234567",
                "-----BEGIN RSA PRIVATE KEY-----",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(detect_secrets.sys, "argv", ["detect_secrets.py", str(secret_file)])

    exit_code = detect_secrets.main()

    out = capsys.readouterr().out.splitlines()
    assert exit_code == 1
    assert any(":1:generic_api_key" in line for line in out)
    assert any(":2:generic_password" in line for line in out)
    assert any(":3:aws_secret_access_key" in line for line in out)
    assert any(":4:base64_secret" in line for line in out)
    assert any(":5:hex_secret" in line for line in out)
    assert any(":6:private_key_header" in line for line in out)


def test_main_skips_allowlisted_and_placeholder_comments(tmp_path, monkeypatch, capsys):
    secret_file = tmp_path / "comments.txt"
    secret_file.write_text(
        "\n".join(
            [
                "# example: AKIAIOSFODNN7EXAMPLE",
                "# pragma: allowlist secret AKIAIOSFODNN7EXAMPLE",
                "# nosecret AKIAIOSFODNN7EXAMPLE",
                "real_key = 'AKIA1234567890ABCDE1'",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(detect_secrets.sys, "argv", ["detect_secrets.py", str(secret_file)])

    exit_code = detect_secrets.main()

    out = capsys.readouterr().out.splitlines()
    assert exit_code == 1
    assert out == [f"{secret_file.resolve()}:4:aws_access_key_id"]


def test_main_skips_markdown_lock_sum_and_binary_files(tmp_path, monkeypatch, capsys):
    markdown = tmp_path / "notes.md"
    lockfile = tmp_path / "package.lock"
    sumfile = tmp_path / "deps.sum"
    binary = tmp_path / "blob.bin"

    markdown.write_text("api_key = 'abcdEFGH1234ijklMNOP5678qrstUVWX'", encoding="utf-8")
    lockfile.write_text("password = 'hunter2-hunter2'", encoding="utf-8")
    sumfile.write_text("aws_secret_access_key = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890abcd'", encoding="utf-8")
    binary.write_bytes(b"\x00api_key=secret")

    monkeypatch.setattr(
        detect_secrets.sys,
        "argv",
        ["detect_secrets.py", str(markdown), str(lockfile), str(sumfile), str(binary)],
    )

    exit_code = detect_secrets.main()

    out = capsys.readouterr().out.splitlines()
    assert exit_code == 0
    assert out == []
