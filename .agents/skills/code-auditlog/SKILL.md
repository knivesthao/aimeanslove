---
name: code-auditlog
description: "Debug logs are not audit logs — auditors ask who did what, and noise is not an answer."
---

# Immutable actor-action-target trail

Create and install a skill named `code-auditlog` (Immutable actor-action-target trail). It instructs the agent as follows: Record actor, action, target, and timestamp as immutable events — debug logs are not audit logs (break-in detection lives in code-logging). Any app with more than one user role — or with money, permissions, or exports — needs this whether or not HIPAA applies; regulated data only makes mandatory what multi-user accountability already requires. Keep the trail append-only with a retention policy and export for auditors. Log permission changes, data exports, and impersonation sessions first; those are the rows auditors ask for. Name the agent in the actor field — 'which agent did this' must be answerable without asking anyone.

## Checks

- immutable actor-action-target events
- retention plus export
- permission and export actions covered
