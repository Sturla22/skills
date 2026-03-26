import importlib.util
import json
from pathlib import Path
import subprocess


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SCAN_DEPENDENCIES_PATH = Path(__file__).resolve().parents[1] / "tools" / "dev" / "scan_dependencies.py"
GENERATE_SBOM_PATH = Path(__file__).resolve().parents[1] / "tools" / "dev" / "generate_sbom.py"

scan_dependencies = load_module(SCAN_DEPENDENCIES_PATH, "scan_dependencies")
generate_sbom = load_module(GENERATE_SBOM_PATH, "generate_sbom")


def test_scan_dependencies_reports_no_external_dependencies_when_directory_is_missing(
    tmp_path, capsys, monkeypatch
):
    monkeypatch.setattr(scan_dependencies, "REPO_ROOT", tmp_path)

    assert scan_dependencies.main() == 0

    assert capsys.readouterr().out.strip() == "No external dependencies found."


def test_scan_dependencies_uses_osv_scanner_when_available(
    tmp_path, capsys, monkeypatch
):
    (tmp_path / "external").mkdir()
    (tmp_path / "external" / "vendor.txt").write_text("dependency\n", encoding="utf-8")
    calls = []

    def fake_which(name: str):
        return name if name == "osv-scanner" else None

    def fake_run(command, cwd=None, check=None, **kwargs):
        calls.append((command, cwd, check, kwargs))
        return subprocess.CompletedProcess(command, 7)

    monkeypatch.setattr(scan_dependencies, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(scan_dependencies.shutil, "which", fake_which)
    monkeypatch.setattr(scan_dependencies.subprocess, "run", fake_run)

    assert scan_dependencies.main() == 7

    assert calls == [
        (["osv-scanner", "--recursive", str(tmp_path / "external")], tmp_path, False, {})
    ]
    assert capsys.readouterr().out.strip() == "Using osv-scanner."


def test_scan_dependencies_falls_back_to_trivy_when_osv_scanner_is_missing(
    tmp_path, capsys, monkeypatch
):
    (tmp_path / "external").mkdir()
    (tmp_path / "external" / "dependency.txt").write_text("present\n", encoding="utf-8")
    calls = []

    def fake_which(name: str):
        return name if name == "trivy" else None

    def fake_run(command, cwd=None, check=None, **kwargs):
        calls.append((command, cwd, check, kwargs))
        return subprocess.CompletedProcess(command, 3)

    monkeypatch.setattr(scan_dependencies, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(scan_dependencies.shutil, "which", fake_which)
    monkeypatch.setattr(scan_dependencies.subprocess, "run", fake_run)

    assert scan_dependencies.main() == 3

    assert calls == [
        (["trivy", "fs", str(tmp_path / "external")], tmp_path, False, {})
    ]
    assert capsys.readouterr().out.strip() == "Using trivy."


def test_scan_dependencies_soft_fails_when_no_scanner_is_available(
    tmp_path, capsys, monkeypatch
):
    (tmp_path / "external").mkdir()
    (tmp_path / "external" / "dependency.txt").write_text("present\n", encoding="utf-8")

    monkeypatch.setattr(scan_dependencies, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(scan_dependencies.shutil, "which", lambda name: None)

    assert scan_dependencies.main() == 0

    assert "No dependency scanner found." in capsys.readouterr().out


def test_generate_sbom_emits_empty_components_when_external_is_missing(
    tmp_path, capsys, monkeypatch
):
    monkeypatch.setattr(generate_sbom, "REPO_ROOT", tmp_path)

    assert generate_sbom.main([]) == 0

    sbom = json.loads(capsys.readouterr().out)
    assert sbom["components"] == []
    assert sbom["bomFormat"] == "CycloneDX"
    assert sbom["specVersion"] == "1.5"
    assert sbom["version"] == 1


def test_generate_sbom_detects_versions_from_external_dependencies(
    tmp_path, capsys, monkeypatch
):
    external = tmp_path / "external"
    (external / "alpha").mkdir(parents=True)
    (external / "alpha" / "VERSION").write_text("1.2.3\n", encoding="utf-8")

    (external / "bravo").mkdir()
    (external / "bravo" / "CMakeLists.txt").write_text(
        "cmake_minimum_required(VERSION 3.25)\nproject(bravo VERSION 2.3.4)\n",
        encoding="utf-8",
    )

    (external / "charlie").mkdir()
    (external / "charlie" / "package.json").write_text(
        json.dumps({"name": "charlie", "version": "3.4.5"}),
        encoding="utf-8",
    )

    (external / "delta").mkdir()
    (tmp_path / ".gitmodules").write_text(
        """
[submodule "delta"]
	path = external/delta
	url = https://example.invalid/delta.git
	branch = main
""".strip()
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(generate_sbom, "REPO_ROOT", tmp_path)

    assert generate_sbom.main([]) == 0

    sbom = json.loads(capsys.readouterr().out)
    components = {component["name"]: component["version"] for component in sbom["components"]}

    assert components == {
        "alpha": "1.2.3",
        "bravo": "2.3.4",
        "charlie": "3.4.5",
        "delta": "main",
    }


def test_generate_sbom_can_write_to_a_file(tmp_path, monkeypatch):
    (tmp_path / "external").mkdir()
    (tmp_path / "external" / "alpha").mkdir()
    output_path = tmp_path / "sbom.json"

    monkeypatch.setattr(generate_sbom, "REPO_ROOT", tmp_path)

    assert generate_sbom.main(["--output", str(output_path)]) == 0

    sbom = json.loads(output_path.read_text(encoding="utf-8"))
    assert sbom["components"] == [
        {"type": "library", "name": "alpha", "version": "unknown"}
    ]
