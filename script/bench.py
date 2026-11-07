#!/usr/bin/env python3
"""Measure per-task skill-pack tokens vs the whole bank.

Each task lists the skills the bank's own routing names for it
(bank map -> area maps -> matched leaves, plus always-on).
Run: .venv/bin/python script/bench.py
"""
import json
from pathlib import Path

import tiktoken

ROOT = Path(__file__).parent.parent
BANK = {s["id"]: s for s in json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))}
ENC = tiktoken.get_encoding("cl100k_base")

TASKS = {
    "login page + API": ["code-index", "ui-index", "code-secure", "code-reuse", "code-token",
                         "code-auth", "code-language", "code-shape", "code-plan",
                         "verify-tests", "verify-visual", "verify-layout"],
    "ingest-to-quality pipeline": ["code-index", "data-index", "code-secure", "code-reuse", "code-token",
                                   "data-ingest", "data-contracts", "data-quality", "code-plan", "verify-tests"],
    "gated deploy setup": ["code-index", "ops-index", "code-secure", "code-reuse", "code-token",
                           "ops-pipeline", "ops-observe", "ops-rollout", "code-plan", "verify-tests"],
    "chart dashboard": ["code-index", "ui-index", "code-secure", "code-reuse", "code-token",
                        "ui-charts", "ui-chart-twin", "code-perf", "verify-tests", "verify-visual"],
}


def tokens(skill):
    s = BANK[skill]
    return len(ENC.encode(s["prompt"] + " " + s["why"] + " " + " ".join(s["checks"])))


def measure():
    total = sum(tokens(i) for i in BANK)
    packs = {}
    for name, skills in TASKS.items():
        missing = [s for s in skills if s not in BANK]
        assert not missing, f"bench task references unknown skills: {missing}"
        pack = sum(tokens(s) for s in skills)
        packs[name] = {"skills": len(skills), "tokens": pack, "share": pack / total}
    return {"bank_skills": len(BANK), "bank_tokens": total, "packs": packs}


def main():
    m = measure()
    print(f"bank skills: {m['bank_skills']}, bank tokens: {m['bank_tokens']}")
    for name, p in m["packs"].items():
        print(f"{name}: {p['skills']} skills, {p['tokens']} tokens, {p['share']:.1%} of bank")


if __name__ == "__main__":
    main()
