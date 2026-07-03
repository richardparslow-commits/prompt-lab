import argparse, re, yaml
from pathlib import Path
from jinja2 import Template

PAT = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

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
