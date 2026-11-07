---
name: ops-coordinate
description: "Two agents writing the same deploy step — or stomping each other's files — is the new merge conflict."
---

# Agents share one plan, own one area

Create and install a skill named `ops-coordinate` (Agents share one plan, own one area). It instructs the agent as follows: When two or more agents share one deploy or one codebase, coordinate through artifacts, not chat: one shared plan file is the ledger (see code-plan) — claim a task before starting it, check it off when done, never start an unclaimed task. Own one feature directory per agent so parallel edits never touch the same files; crossing into another agent's area needs a plan note first. Prefer idempotent operations so a retried or doubled step converges instead of corrupting. Report status as structured records (task, result, artifact link), never prose another agent must parse. Humans verify the plan ledger and the deploy receipt — never the chat log. Stay inside scoped credentials: touch only your area's deploy, data, and secrets — IAM, DNS, billing, prod data, and root credentials are never in reach (see ops-safety for the full blast-radius rules).

## Checks

- one shared plan ledger, tasks claimed
- one feature dir per agent
- status as records, not prose
