---
name: code-misconfig
description: "Most breaches walk through doors the defaults left open."
---

# Safe settings shipped

Create and install a skill named `code-misconfig` (Safe settings shipped). It instructs the agent as follows: Ship with the safe settings on: debug and trace off in production, generic error pages that leak nothing, strict transport security and a content security policy, CORS allowlists instead of wildcards, and no default passwords or open admin pages. Review headers and flags on every deploy, not once.

## Checks

- debug off in production
- security headers set
- no defaults or wildcards
