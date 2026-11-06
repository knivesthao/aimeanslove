---
name: code-polyglot
description: "Guest code fails at the seam and in language-specific traps the Python-trained agent walks into."
---

# Own guest-language code safely

Create and install a skill named `code-polyglot` (Own guest-language code safely). It instructs the agent as follows: Use this only for code the house language technically cannot carry — Python remains the default everywhere else. Define the seam first: the contract lives in one repo as protobuf or JSON schema, and both sides generate from it — never hand-write both ends. Test the seam with recorded fixtures in the caller's language; the guest service proves itself with its own native tests, run with its native command (go test, cargo test, mix test). Keep guest code small and boring — the hot path only, everything else stays in Python. Agent pitfalls per guest: Rust — restructure ownership instead of cloning to satisfy the borrow checker. Go — propagate context and wrap errors; never swallow err. Erlang and Elixir — supervision trees own restarts, so don't defensively trap what the supervisor replays; keep state in processes.

## Checks

- seam defined as generated contract
- seam tests with recorded fixtures
- guest code minimal, hot path only
