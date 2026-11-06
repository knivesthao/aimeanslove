---
name: ops-oncall
description: "The single-hero pager with no notes guarantees the same incident repeats."
---

# Rotation, runbooks, tracked postmortems

Create and install a skill named `ops-oncall` (Rotation, runbooks, tracked postmortems). It instructs the agent as follows: Page a scheduled rotation with escalation paths and severity levels — never a single hero with no notes (page-worthy symptoms live in ops-observe). Every page links its runbook; pages without runbooks get written during the incident review. Blameless postmortems within days, action items tracked to done — the review nobody reads is the incident that repeats.

## Checks

- scheduled rotation with escalation
- runbook per page
- postmortems tracked to done
