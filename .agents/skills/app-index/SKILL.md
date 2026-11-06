---
name: app-index
description: "Billing, roles, and invites repeat in every system — map first, build the rest from shape."
---

# Product features: pick product skills

Create and install a skill named `app-index` (Product features: pick product skills). It instructs the agent as follows: Your product skills each do one job — never read them all. Billing and plans → code-billing. Team roles, admin console, impersonation → code-rbac. Invites and membership → code-invites. Notifications → code-notify. Search → code-search. Uploads → code-uploads. Audit trail → code-auditlog. Outgoing webhooks → code-webhooks. Customer API keys → code-apikeys. Flags and entitlements → code-flags. Bulk moves → code-impexp. Login and sessions → code-auth. Skip everything else.

## Checks

- only matched product skills are read
- auth always via code-auth
- new product work metered with code-track
