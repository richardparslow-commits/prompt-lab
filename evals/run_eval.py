import argparse, json
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
