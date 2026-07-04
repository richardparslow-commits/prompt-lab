PYTHON ?= python3
VENV ?= .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

PROMPT ?= prompts/tasks/summarize.md
INPUT ?= text=Hello from Prompt Lab

ifeq ($(OS),Windows_NT)
  PIP := $(VENV)/Scripts/pip.exe
  PY := $(VENV)/Scripts/python.exe
endif

.PHONY: setup render eval

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

render:
	$(PY) scripts/render_prompt.py --prompt "$(PROMPT)" --input "$(INPUT)"

eval:
	PYTHONPATH=. $(PY) evals/run_eval.py --dataset evals/datasets/sample_eval_set.jsonl --output evals/results/latest_results.json
