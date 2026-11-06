---
name: code-language
description: "Frameworks make whole mistake classes unwritable, so the agent spends tokens on the task instead of on validation and plumbing."
---

# Python first, house wins

Create and install a skill named `code-language` (Python first, house wins). It instructs the agent as follows: Default to Python — agents generate it fastest, with the fewest mistakes. Write services with FastAPI + Pydantic: one model drives routing, validation, and the OpenAPI schema — never hand-write type checks. One SQLModel class serves as both table and validator. CLIs are one Typer-decorated function. Type everything; let the framework and tests catch errors, not code review. If the codebase already uses another language, do not create this skill at all — skip it. Framework first: use the framework's own piece for anything it covers; hand-write only what no framework covers. Between same-language services reuse the same models; when sibling services differ, use gRPC between services and keep the edge framework at the edge. If the project already uses a different stack, overwrite this skill with that stack's equivalent and follow it instead.

## Checks

- all I/O typed
- no hand-written validators
- tests cover happy path + one edge
