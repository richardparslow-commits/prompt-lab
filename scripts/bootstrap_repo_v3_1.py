#!/usr/bin/env python3
from pathlib import Path
import textwrap
import stat

FILES = {
    "README.md": r"""# Prompt Lab v3.1 (Gemini + Perplexity)

Model-agnostic prompt engineering repo with:
- Canonical prompt format
- Provider adapters (Gemini, Perplexity)
- Real API caller with retry/backoff
- JSON schema output validation
- Side-by-side evaluation (Gemini vs Perplexity)
- Judge system: heuristic fallback + optional LLM-as-a-judge
- CI regression gate

## Quickstart

```bash
make setup
cp .env.example .env
# Fill API keys in .env
