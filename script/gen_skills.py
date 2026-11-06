#!/usr/bin/env python3
"""Generate .agents/skills/<id>/SKILL.md from skills.json (single source).

Run: .venv/bin/python script/gen_skills.py
Never hand-edit the generated files; edit skills.json and re-run.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
BANK = json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))
DEST = ROOT / ".agents" / "skills"


def q(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


for skill in BANK:
    directory = DEST / skill["id"]
    directory.mkdir(parents=True, exist_ok=True)
    checks = "\n".join("- " + c for c in skill["checks"])
    body = (
        "---\n"
        f"name: {skill['id']}\n"
        f"description: {q(skill['why'])}\n"
        "---\n\n"
        f"# {skill['title']}\n\n"
        f"{skill['prompt']}\n\n"
        "## Checks\n\n"
        f"{checks}\n"
    )
    (directory / "SKILL.md").write_text(body, encoding="utf-8")
    print("wrote", directory.relative_to(ROOT))
