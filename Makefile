.PHONY: init serve
SHELL := /bin/bash

init:
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

serve:
	source .venv/bin/activate && mkdocs serve
