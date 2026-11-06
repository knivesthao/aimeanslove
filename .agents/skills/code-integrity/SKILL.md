---
name: code-integrity
description: "A build that can't prove what it contains can't prove what it ships."
---

# Verify before trust

Create and install a skill named `code-integrity` (Verify before trust). It instructs the agent as follows: Trust nothing you didn't verify: lockfiles pin the whole tree, webhook handlers check signatures before acting, CI runs tests before deploys, and installs come from registries — never pipe a URL to a shell. If bytes changed without a commit, stop and ask.

## Checks

- lockfiles committed
- webhook signatures verified
- no curl-to-shell installs
