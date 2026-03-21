PYTHON ?= python3
CI_TOOLS_DIR := tools/ci

.PHONY: sync-agents check-agents link smoke-cli test check-layout install-pre-commit run-pre-commit check-pre-commit-config ci-bootstrap-ubuntu check-static-analysis check-cmake-starter ci-checks

sync-agents:
	$(PYTHON) tools/cli.py sync

check-agents:
	$(PYTHON) tools/cli.py sync --check

link:
	$(PYTHON) tools/cli.py sync --link

smoke-cli:
	$(PYTHON) tools/cli.py --help > /dev/null

test:
	$(PYTHON) -m pytest -q

check-layout:
	$(PYTHON) tools/cli.py check-layout

install-pre-commit:
	$(PYTHON) -m pip install --user pre-commit
	$(PYTHON) tools/dev/install_pre_commit.py

run-pre-commit:
	$(PYTHON) -m pre_commit run --all-files

check-pre-commit-config:
	$(PYTHON) -m pre_commit validate-config

ci-bootstrap-ubuntu:
	$(CI_TOOLS_DIR)/bootstrap-ubuntu.sh

check-static-analysis:
	$(PYTHON) $(CI_TOOLS_DIR)/check-static-analysis.py

check-cmake-starter:
	$(CI_TOOLS_DIR)/check-cmake-starter.sh

ci-checks: check-agents smoke-cli test check-layout check-pre-commit-config check-static-analysis check-cmake-starter
