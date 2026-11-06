---
name: sec-sso
description: "Permanent break-glass exceptions and legacy logins are the doors attackers walk through."
---

# One IdP, expiring exceptions

Create and install a skill named `sec-sso` (One IdP, expiring exceptions). It instructs the agent as follows: Route every login through one identity provider — workforce and enterprise customers alike (app basics live in code-auth). Require phishing-resistant MFA; expire legacy password-only logins and break-glass exceptions with a date, never permanently. Provision just-in-time on first login from verified domains; deprovision automatically on IdP removal. Every exception carries an owner, an expiry, and an audit trail.

## Checks

- one IdP, no permanent exceptions
- JIT provision, auto deprovision
- exceptions owned, expiring, audited
