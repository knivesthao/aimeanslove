---
name: ops-safety
description: "Fast agents with prod access convert mistakes into outages at machine speed."
---

# Blast radius first, speed second

Create and install a skill named `ops-safety` (Blast radius first, speed second). It instructs the agent as follows: Scope every agent's credentials least-privilege: an agent touches only its area's deploy, data, and secrets — IAM, DNS, billing, prod data, and root credentials are never in an agent's reach. Destructive ops (data deletes, infra teardown, mass revocation) need a second approver, human or agent, before executing — no exceptions, only a faster approval path for emergencies. An actor whose deploys fail twice in a row loses deploy rights automatically, like a drained host, until a human reinstates them. Cap what agents may spend: budgets with alerts and kill switches on agent-driven cloud actions.

## Checks

- agents scoped, never-touch list enforced
- destructive ops need a second approver
- failing actors auto-drained, spend capped
