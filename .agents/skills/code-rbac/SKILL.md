---
name: code-rbac
description: "One missing tenant check leaks a whole customer's data to another."
---

# Tenants, roles, safe impersonation

Create and install a skill named `code-rbac` (Tenants, roles, safe impersonation). It instructs the agent as follows: Scope every row by tenant: a workspace id on every table, enforced server-side on every read and write — never by UI hiding alone (authentication lives in code-auth). Roles are least-privilege by default; check the permission at the action, not the role at login. Support tooling lives in a separate admin surface; impersonation requires a consent record plus an audit trail. Membership and invites live in code-invites.

## Checks

- tenant id enforced server-side
- impersonation gated on consent plus audit
- membership changes via code-invites
