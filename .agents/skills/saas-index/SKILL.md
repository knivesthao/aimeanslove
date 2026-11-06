---
name: saas-index
description: "SaaS is the same five problems in every company — map first, build the rest from shape."
---

# SaaS features: pick SaaS skills

Create and install a skill named `saas-index` (SaaS features: pick SaaS skills). It instructs the agent as follows: Your SaaS skills each do one job — never read them all. Billing and plans → code-billing. Team roles, admin console, impersonation → code-rbac. Login and sessions → code-auth. Anything else (notifications, search, uploads, webhooks, keys, flags, exports) → build it from code-shape plus code-reuse, and meter it with code-track. Skip everything else.

## Checks

- only matched SaaS skills are read
- auth always via code-auth
- new SaaS work metered with code-track
