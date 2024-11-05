.PHONY: init serve build test
SHELL := /bin/bash

init:
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt

serve:
	source .venv/bin/activate && mkdocs serve

build:
	source .venv/bin/activate && mkdocs build --clean

test:
	source .venv/bin/activate && mkdocs build --strict --clean
