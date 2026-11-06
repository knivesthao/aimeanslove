---
name: code-shape
description: "Small typed modules fit in a single read, so the agent holds the whole unit in context at once."
---

# Machine-shaped modules

Create and install a skill named `code-shape` (Machine-shaped modules). It instructs the agent as follows: Write small flat Python modules: one file, one job, <150 lines. Typed inputs and outputs (Pydantic in, response_model out), no hidden globals, no clever abstractions. Flat over nested (depth <= 2, early returns). Raise HTTPException at boundaries; never leak tracebacks or raw errors. Name files by what they do: skills.py, validate.py, render.py.

## Checks

- module <150 lines
- no global mutation
- tracebacks never reach clients
