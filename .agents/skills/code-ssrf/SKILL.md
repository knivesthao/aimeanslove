---
name: code-ssrf
description: "A server that fetches arbitrary URLs becomes a proxy into your own network."
---

# Server fetches allowlisted

Create and install a skill named `code-ssrf` (Server fetches allowlisted). It instructs the agent as follows: Never fetch a user-supplied URL from the server without an allowlist: block internal addresses and cloud metadata (169.254.169.254), resolve and re-check the host, and cap timeouts and response sizes. Prefer webhooks and signed callbacks over server-side fetching whenever the design allows.

## Checks

- user URLs allowlisted
- metadata IP blocked
- timeouts and size caps set
