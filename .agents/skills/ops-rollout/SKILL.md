---
name: ops-rollout
description: "Shipping 100% at once with no rollback trigger turns every bad deploy into a full outage."
---

# Progressive traffic, predefined rollback

Create and install a skill named `ops-rollout` (Progressive traffic, predefined rollback). It instructs the agent as follows: Shift traffic progressively — canary then staged percentages — with health gates promoting each step. Define the rollback trigger before starting; rollback is one action that restores the last good version in minutes. Never 100% at once outside an emergency, and emergencies get a postmortem.

## Checks

- health-gated progressive steps
- rollback trigger predefined
- rollback in minutes
