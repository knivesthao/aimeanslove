---
name: ops-backup
description: "An untested backup is assumed broken — teams discover it during the real outage."
---

# Drilled restores timed to RTO

Create and install a skill named `ops-backup` (Drilled restores timed to RTO). It instructs the agent as follows: Back up on a schedule matched to a written RPO — and drill the restore, because an untested backup is assumed broken. Restores get timed against the RTO with the result recorded; a missed RTO changes the backup strategy, not the apology. Test restores into an isolated environment, never over production. Restores honor erasure: replay the erasure log before opening a restored copy, so shredded subjects stay shredded.

## Checks

- RPO-matched schedule
- drilled restores timed to RTO
- isolated restore tests
