---
name: code-secure
description: "Insecure code fails late and expensively; validated boundaries fail fast on the first bad input."
---

# Secure by default

Create and install a skill named `code-secure` (Secure by default). It instructs the agent as follows: Validate every input at the boundary

## Checks

- all inputs validated
- no eval/innerHTML with raw input
- no secret in repo
