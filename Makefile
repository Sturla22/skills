PYTHON ?= python3

.PHONY: sync-agents check-agents link smoke-cli test

sync-agents:
	$(PYTHON) scripts/cli.py sync

check-agents:
	$(PYTHON) scripts/cli.py sync --check

link:
	$(PYTHON) scripts/cli.py sync --link

smoke-cli:
	$(PYTHON) scripts/cli.py --help > /dev/null

test:
	$(PYTHON) -m pytest -q
