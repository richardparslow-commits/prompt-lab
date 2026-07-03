from pathlib import Path

files = {
"Makefile": """PYTHON ?= python3
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
\t$(PYTHON) -m venv $(VENV)
\t$(PIP) install --upgrade pip
\t$(PIP) install -r requirements.txt

render:
\t$(PY) scripts/render_prompt.py --prompt "$(PROMPT)" --input "$(INPUT)"

eval:
\t$(PY) evals/run_eval.py --dataset evals/datasets/sample_eval_set.jsonl --output evals/results/latest_results.json
""",

"requirements.txt": """PyYAML==6.0.2
Jinja2==3.1.4
python-dotenv==1.0.1
requests==2.32.3
jsonschema==4.23.0
""",

"scripts/render_prompt.py": """import argparse, re, yaml
from pathlib import Path
from jinja2 import Template

PAT = re.compile(r"^---\\n(.*?)\\n---\\n(.*)$", re.DOTALL)

def load_prompt_file(path: Path):
    c = path.read_text(encoding="utf-8")
    m = PAT.match(c)
    if not m:
        raise ValueError(f"Invalid frontmatter: {path}")
    meta, body = m.groups()
    return (yaml.safe_load(meta) or {}, body.strip())

def parse_kv_pairs(items):
    out = {}
    for p in items or []:
        if "=" not in p:
            raise ValueError(f"Invalid --input {p}; use key=value")
        k,v = p.split("=",1)
        out[k]=v
    return out

def render_with_inputs(meta, body, inputs):
    missing=[]
    for i in meta.get("inputs",[]):
        if i.get("required") and i.get("name") not in inputs:
            missing.append(i.get("name"))
    if missing:
        raise ValueError(f"Missing required inputs: {missing}")
    return Template(body).render(**inputs)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--input", action="append", default=[])
    a = ap.parse_args()
    meta, body = load_prompt_file(Path(a.prompt))
    print(render_with_inputs(meta, body, parse_kv_pairs(a.input)))
""",

"evals/run_eval.py": """import argparse, json
from pathlib import Path
from scripts.render_prompt import load_prompt_file, render_with_inputs

def run(dataset, output):
    rows = [json.loads(x) for x in Path(dataset).read_text(encoding="utf-8").splitlines() if x.strip()]
    results = []
    for r in rows:
        meta, body = load_prompt_file(Path(r["prompt"]))
        rendered = render_with_inputs(meta, body, r["inputs"])
        results.append({"case_id": r["case_id"], "rendered_preview": rendered[:200]})
    out = {"num_cases": len(results), "results": results}
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    run(a.dataset, a.output)
""",

"prompts/tasks/summarize.md": """---
id: summarize_v1
goal: "Summarize text into 5 bullets"
inputs:
  - name: text
    required: true
---
Summarize the following into exactly 5 concise bullet points:

{{ text }}
""",

"evals/datasets/sample_eval_set.jsonl": """{"case_id":"sum_001","prompt":"prompts/tasks/summarize.md","inputs":{"text":"Acme revenue grew 18% to $42M; margin improved from 12% to 16%; risks include EMEA slowdown."}}
""",
"evals/results/.gitkeep": ""
}

for p, c in files.items():
    path = Path(p)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(c, encoding="utf-8")

print("Scaffold repaired.")
