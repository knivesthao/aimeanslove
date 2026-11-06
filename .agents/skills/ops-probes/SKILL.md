---
name: ops-probes
description: "Instant-healthy sends traffic to broken pods mid-deploy; conflated probes restart what should drain."
---

# Liveness split from readiness

Create and install a skill named `ops-probes` (Liveness split from readiness). It instructs the agent as follows: Separate liveness (restart me) from readiness (send me traffic): a pod that cannot serve stays alive but out of rotation. Probes check real dependencies with timeouts — instant-healthy sends traffic to broken pods mid-deploy. Failing readiness sheds load; failing liveness restarts. Never probe with the same handler that serves users.

## Checks

- liveness split from readiness
- probes check real deps
- no user-handler probes
