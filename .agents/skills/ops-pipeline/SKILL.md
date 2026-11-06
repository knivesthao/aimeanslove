---
name: ops-pipeline
description: "Hand-rolled pipelines drift until the deploy that matters most is the one least tested."
---

# One template, gated deploys, one-button rollback

Create and install a skill named `ops-pipeline` (One template, gated deploys, one-button rollback). It instructs the agent as follows: Deploy only from one shared templated pipeline — never hand-rolled per repo. Required gates in order: build, tests, security scan, approval for production. Every deploy links to its commit; every PR gets an ephemeral preview environment that auto-stops when idle. Rollback means redeploying the previous known-good artifact with one action — never a new build under fire. Block on critical scan findings; ticket the rest with SLAs.

## Checks

- one shared template, no hand-rolled pipes
- preview envs auto-stop
- rollback is one action on an old artifact
