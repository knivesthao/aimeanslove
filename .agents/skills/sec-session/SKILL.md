---
name: sec-session
description: "Long-lived JWTs with no revocation path stay valid after theft — the classic breach extender."
---

# Short-lived revocable sessions

Create and install a skill named `sec-session` (Short-lived revocable sessions). It instructs the agent as follows: Issue short-lived tokens with rotation and binding; keep server-side revocation so stolen sessions die on demand. Absolute lifetimes cap every session no matter how active. App login mechanics live in code-auth; this skill governs lifetimes and kill paths.

## Checks

- short-lived with rotation
- server-side revocation
- absolute lifetime caps
