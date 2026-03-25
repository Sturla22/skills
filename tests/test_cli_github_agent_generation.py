import importlib.util
from pathlib import Path


CLI_PATH = Path(__file__).resolve().parents[1] / "tools" / "cli.py"
CLI_SPEC = importlib.util.spec_from_file_location("repo_cli", CLI_PATH)
assert CLI_SPEC is not None
assert CLI_SPEC.loader is not None
cli = importlib.util.module_from_spec(CLI_SPEC)
CLI_SPEC.loader.exec_module(cli)


def test_generate_github_agent_includes_model_when_spec_sets_copilot_model():
    spec = {
        "name": "planner",
        "description": "Creates detailed plans",
        "body": "You are the planner.",
        "copilot_model": "gpt-5.4",
    }

    generated = cli._generate_github_agent(spec)

    assert 'model: "gpt-5.4"' in generated


def test_generate_github_agent_omits_model_when_spec_has_no_copilot_model():
    spec = {
        "name": "planner",
        "description": "Creates detailed plans",
        "body": "You are the planner.",
    }

    generated = cli._generate_github_agent(spec)

    assert "model:" not in generated
