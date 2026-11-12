PYTHON ?= python3
SET ?= l06_security
PROFILE ?= lesson-06
GATE ?= all

.PHONY: eval validate

eval:
	$(PYTHON) cli.py --set "$(SET)" --profile "$(PROFILE)" --gate "$(GATE)" --traces

validate:
	$(PYTHON) cli.py --set "$(SET)" --gate "$(GATE)" --dry-run
