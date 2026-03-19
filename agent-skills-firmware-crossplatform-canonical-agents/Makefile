PYTHON ?= python3

.PHONY: sync-agents check-agents

sync-agents:
	$(PYTHON) scripts/sync_agent_layouts.py

check-agents:
	$(PYTHON) scripts/sync_agent_layouts.py --check
