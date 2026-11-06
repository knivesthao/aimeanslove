---
name: code-cache
description: "A cache hit skips work entirely — the cheapest token is the one never spent."
---

# Cache in layers, swap the store

Create and install a skill named `code-cache` (Cache in layers, swap the store). It instructs the agent as follows: Cache in layers, nearest first: HTTP (ETag plus 304, Cache-Control per content type), in-process memo for hot reads, CDN edge in front. Hide every layer behind one tiny interface — get, set, invalidate — so the store swaps without touching callers: memory today, Redis or Memcached tomorrow. Cache computed answers, never user-specific secrets. Invalidate on write (data changed), not on a timer alone.

## Checks

- ETag and 304 on repeat reads
- one interface, swappable store
- invalidation tied to writes
