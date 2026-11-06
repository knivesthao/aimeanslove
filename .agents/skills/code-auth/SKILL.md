---
name: code-auth
description: "Authentication is the most-broken OWASP category; one shared login path removes the whole class."
---

# Login and permissions

Create and install a skill named `code-auth` (Login and permissions). It instructs the agent as follows: Logins use signed cookies (built into Starlette — one secret key, no extra package). Sign in with Google uses authlib. Services talking to each other use JWTs via pyjwt. Passwords are checked with bcrypt via passlib — never write your own password check, because a wrong one fails silently and an agent will not notice. For every action, check the permission at the boundary and default to deny: never trust a role or user id sent by the client, always re-check it on the server.

## Checks

- sessions are signed cookies
- passwords via bcrypt only
- permission checked per action, default deny
