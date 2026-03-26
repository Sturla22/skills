import argparse
import importlib.util
from pathlib import Path


CLI_PATH = Path(__file__).resolve().parents[1] / "tools" / "cli.py"
CLI_SPEC = importlib.util.spec_from_file_location("repo_cli", CLI_PATH)
assert CLI_SPEC is not None
assert CLI_SPEC.loader is not None
cli = importlib.util.module_from_spec(CLI_SPEC)
CLI_SPEC.loader.exec_module(cli)


def test_build_parser_registers_new_postmortem_and_check_debt():
    parser = cli.build_parser()
    subparsers = next(
        action for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    )

    assert "new-postmortem" in subparsers.choices
    assert "check-debt" in subparsers.choices


def test_new_postmortem_creates_next_numbered_file(tmp_path, monkeypatch):
    work_id = "demo"
    packet_dir = tmp_path / "docs" / "work" / work_id
    evidence_dir = packet_dir / "evidence"
    evidence_dir.mkdir(parents=True)
    (evidence_dir / "postmortem-001.md").write_text("one", encoding="utf-8")
    (evidence_dir / "postmortem-002.md").write_text("two", encoding="utf-8")

    monkeypatch.setattr(cli, "DOCS_WORK_DIR", tmp_path / "docs" / "work")
    monkeypatch.setattr(cli, "_read_template", lambda name: f"template:{name}")

    written = {}

    def fake_write_new_file(dest: Path, content: str) -> None:
        written["dest"] = dest
        written["content"] = content

    monkeypatch.setattr(cli, "_write_new_file", fake_write_new_file)

    cli.cmd_new_postmortem(argparse.Namespace(work_id=work_id))

    assert written["dest"] == evidence_dir / "postmortem-003.md"
    assert written["content"] == "template:postmortem-template.md"


def test_check_debt_reports_counts_by_status(tmp_path, monkeypatch, capsys):
    root = tmp_path
    debt_file = root / "docs" / "tech-debt.md"
    debt_file.parent.mkdir(parents=True)
    debt_file.write_text(
        "\n".join([
            "## TD-001 Remove legacy workaround",
            "**Status**: open",
            "",
            "## TD-002 Simplify cache invalidation",
            "**Status**: Resolved",
            "",
            "## Deferred cleanup",
            "This section tracks TD-003 for later.",
            "**Status**: deferred",
        ]),
        encoding="utf-8",
    )

    monkeypatch.setattr(cli, "ROOT", root)

    cli.cmd_check_debt(argparse.Namespace(root=None))

    out = capsys.readouterr().out
    assert "OPEN DEBT:" in out
    assert "  TD-001" in out
    assert "DEFERRED DEBT:" in out
    assert "  TD-003" in out
    assert "RESOLVED DEBT:" in out
    assert "  TD-002" in out
    assert "Result: 3 item(s) tracked — 1 open, 1 deferred, 1 resolved — OK" in out
