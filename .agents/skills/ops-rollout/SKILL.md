---
name: ops-rollout
description: "Shipping 100% at once with no rollback trigger turns every bad deploy into a full outage."
---

# Progressive traffic, predefined rollback

Create and install a skill named `ops-rollout` (Progressive traffic, predefined rollback). It instructs the agent as follows: Shift traffic progressively — canary then staged percentages — with health gates promoting each step. Define the rollback trigger before starting; rollback is one action that restores the last good version in minutes. Compare canary metrics against the baseline automatically before each promotion — progressive without comparison is just slow. Roll back stateless, roll forward stateful: data never goes back, only forward with a fix. Never 100% at once outside an emergency; emergencies are declared by a human, and every one gets a postmortem. Compare canary against baseline automatically before each promotion: error rate, p95 latency, and saturation versus the pre-deploy window — halt if errors exceed baseline by more than a point, p95 climbs over twenty percent, or any SLO burns; a halt pages the alert owner with both windows attached, and promotion never resumes without a human.

## Checks

- health-gated progressive steps
- rollback trigger predefined
- rollback in minutes
