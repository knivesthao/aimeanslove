---
name: data-concurrency
description: "Two writers plus no locking equals lost updates — the bug that only appears in production."
---

# Concurrent writers converge, never clobber

Create and install a skill named `data-concurrency` (Concurrent writers converge, never clobber). It instructs the agent as follows: Wrap multi-record changes in one database transaction — partial writes are corruption, not an edge case. Prefer optimistic locking: a version column on contested rows, retry the whole transaction on version mismatch, never hold a pessimistic lock across network calls. Make every write idempotent (see data-ingest) so the retry is safe to run twice. Shard hot rows — a single counter row updated by thousands of writers serializes everything; aggregate shards or buffer increments instead. Accept the database as the adult in the room: uniqueness, foreign keys, and check constraints enforced by the store beat application-level checks that race. Know your isolation default and what it hides; escalate only the transaction that proved it needs more.

## Checks

- multi-record changes in one transaction
- optimistic locking with retry, no held locks
- hot rows sharded, not hammered
