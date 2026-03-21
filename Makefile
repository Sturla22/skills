PYTHON ?= python3

.PHONY: sync-agents check-agents link smoke-cli test check-layout

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
