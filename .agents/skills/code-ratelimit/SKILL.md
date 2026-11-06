---
name: code-ratelimit
description: "An unthrottled endpoint is a counter-inflation and outage tool for anyone with a loop."
---

# Throttle the expensive doors

Create and install a skill named `code-ratelimit` (Throttle the expensive doors). It instructs the agent as follows: Throttle expensive endpoints per client: a sliding window (for example 120 requests per minute per IP on API routes) — public reads get room, writes and beacons get less. Answer over-limit with 429 plus a Retry-After header, never a crash page. Keep limits in config, not code, so they change without a deploy. Count blocked requests separately so attacks show up in stats instead of hiding in totals. Behind a CDN, prefer its edge rules; the built-in limiter is the second layer, not the first.

## Checks

- expensive routes throttled per client
- 429 carries Retry-After
- limits live in config
