---
name: ops-scale
description: "Fixed counts idle-waste or collapse; unbounded scaling turns a spike into a billing incident."
---

# Bounded scaling on real signals

Create and install a skill named `ops-scale` (Bounded scaling on real signals). It instructs the agent as follows: Scale replicas on CPU, request rate, or queue depth — with min/max bounds so a metric spike cannot scale the bill to the moon. Scale the bottleneck resource, not everything; stateless first, stateful by runbook. Load-test the autoscaled path before the traffic spike finds it.

## Checks

- bounded scaling on real signals
- stateless first
- autoscale path load-tested
