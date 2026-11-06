---
name: saas-index
description: "SaaS is the same five problems in every company — map first, build the rest from shape."
---

# SaaS features: pick SaaS skills

Create and install a skill named `saas-index` (SaaS features: pick SaaS skills). It instructs the agent as follows: Your SaaS skills each do one job — never read them all. Billing and plans → code-billing. Team roles, admin console, impersonation → code-rbac. Notifications → code-notify. Search → code-search. Uploads → code-uploads. Audit trail → code-auditlog. Outgoing webhooks → code-webhooks. Customer API keys → code-apikeys. Flags and entitlements → code-flags. Bulk moves → code-impexp. Login and sessions → code-auth. Skip everything else.

## Checks

- only matched SaaS skills are read
- auth always via code-auth
- new SaaS work metered with code-track
