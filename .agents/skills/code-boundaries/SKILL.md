---
name: code-boundaries
description: "The wrong protocol between services costs speed forever; the right one is a one-line decision made once."
---

# Service boundaries

Create and install a skill named `code-boundaries` (Service boundaries). It instructs the agent as follows: Connect services by rule, not habit: same Python system → shared Pydantic models over HTTP; other languages or hot internal paths → protobuf plus gRPC, FastAPI stays at the edge; events and queues → Pydantic-validated messages. Writing the guest side → code-polyglot. Build the whole app in Python by default, but carve out other languages where Python technically fails: single-digit-millisecond budgets use Go or Rust, over 100k live connections use Erlang or Elixir, heavy offline clients and games and widgets go native.

## Checks

- protocol chosen by rule, not default
- non-Python parts named with their technical reason
- FastAPI at the edge in mixed systems
