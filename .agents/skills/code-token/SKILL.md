---
name: code-token
description: "Every token spent writing or re-reading code is a token not spent on the task; cheap code compounds across sessions."
---

# Token-efficient code

Create and install a skill named `code-token` (Token-efficient code). It instructs the agent as follows: Write code that's cheap to generate and cheap to re-read: type everything, one canonical pattern per job (FastAPI route, Pydantic model, Typer command). Early returns, table-driven branches over nested ifs, JSON-first data. Delete dead code — every dead line taxes every future read. Prefer 20 lines of plain code over 5 lines of clever code.

## Checks

- no nested depth >2
- no dead exports
- single pattern per job
