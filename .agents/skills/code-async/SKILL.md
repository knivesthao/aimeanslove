---
name: code-async
description: "Blocking the request on slow work times out users and cascades; unbounded fan-out stampedes everything downstream."
---

# Slow work leaves the request

Create and install a skill named `code-async` (Slow work leaves the request). It instructs the agent as follows: Default to synchronous for reads the user waits on — async is for work that outlives attention, not a faster way to do the same call. Hand slow work to a queue with a worker (see ops-pipeline for the deploy side): return a job id immediately, notify on completion like code-notify does, never hold the request open. Fan out with bounded concurrency — a fixed worker pool or semaphore, never unbounded spawns that stampede the downstream; gather results, and decide upfront whether one failure fails the batch or ships partial. CPU-bound work goes to a process pool, IO-bound to async tasks. Every background job is retryable and idempotent (see data-ingest), with its own stall SLA (see data-orchestrate); a silent dead worker is the failure mode.

## Checks

- slow work leaves the request with a job id
- fan-out bounded, failure policy declared
- background jobs retryable with stall SLAs
