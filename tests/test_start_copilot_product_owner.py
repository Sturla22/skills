import importlib.util
from pathlib import Path


SCRIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "dev"
    / "start_copilot_product_owner.py"
)
SCRIPT_SPEC = importlib.util.spec_from_file_location(
    "start_copilot_product_owner",
    SCRIPT_PATH,
)
assert SCRIPT_SPEC is not None
assert SCRIPT_SPEC.loader is not None
launcher = importlib.util.module_from_spec(SCRIPT_SPEC)
SCRIPT_SPEC.loader.exec_module(launcher)


def test_build_copilot_command_prepends_product_owner_agent():
    command = launcher.build_copilot_command(["--resume"])

    assert command == ["copilot", "--agent", "product-owner", "--resume"]


def test_build_copilot_command_preserves_interactive_prompt_args():
    command = launcher.build_copilot_command(
        ["-i", "Summarize the current instructions."]
    )

    assert command == [
        "copilot",
        "--agent",
        "product-owner",
        "-i",
        "Summarize the current instructions.",
    ]


def test_build_copilot_command_rejects_explicit_agent_override():
    try:
        launcher.build_copilot_command(["--agent", "developer"])
    except ValueError as exc:
        assert "always starts Copilot" in str(exc)
    else:
        raise AssertionError("Expected ValueError when overriding --agent")


def test_build_copilot_command_rejects_inline_agent_override():
    try:
        launcher.build_copilot_command(["--agent=developer"])
    except ValueError as exc:
        assert "always starts Copilot" in str(exc)
    else:
        raise AssertionError("Expected ValueError when overriding --agent")
