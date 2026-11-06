---
name: verify-tests
description: "Tests are the only verdict both humans and agents can trust without reading the code."
---

# Tests are the spec

Create and install a skill named `verify-tests` (Tests are the spec). It instructs the agent as follows: Humans judge by tests, not by reading code. Ship one runnable check per behavior: one command (`./run.sh test`, `pytest`) must pass. Cover happy path + one edge (empty, oversized, unauthorized). Print PASS/FAIL lines an agent can parse.

## Checks

- one command runs all checks
- edge case covered
- output is parseable
