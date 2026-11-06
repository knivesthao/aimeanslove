---
name: code-fallback
description: "Systems die when everything is equally critical; rank first, shed in order."
---

# Shed load, keep serving

Create and install a skill named `code-fallback` (Shed load, keep serving). It instructs the agent as follows: Rank every feature by criticality before trouble arrives: core serves, nice-to-haves shed first. Put each sheddable feature behind a flag so it turns off without a deploy. Under stress, serve stale cache, pause polling and beacons, and answer 429 with Retry-After on what's left — never crash the core to save the extras. Prove it with a stress test at multiples of peak load; an untested fallback is a wish. Group code by feature (see code-group) so a shed feature — or a future service split — follows existing seams instead of new surgery.

## Checks

- features ranked by criticality
- shedding is flag-gated, not a deploy
- stress test proves the degraded mode
