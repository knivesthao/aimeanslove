---
name: code-reuse
description: "Every line the agent doesn't write is tokens never spent and bugs never made."
---

# Reuse before you build

Create and install a skill named `code-reuse` (Reuse before you build). It instructs the agent as follows: Before writing anything new, look for a piece that already does the job: search the repo first, then the stack's own library — Flowbite components, Lucide icons, Lit or WebAwesome pieces, FastAPI and Pydantic helpers. Use the found piece as-is and adapt only what the task needs. When the same markup or logic appears twice, pull it into one shared helper or component where the next agent will find it — never paste a third copy. Hand-write only what no existing piece covers.

## Checks

- no hand-built copy of a stocked piece
- repeated markup lives in one helper
- new pieces placed where agents will find them
