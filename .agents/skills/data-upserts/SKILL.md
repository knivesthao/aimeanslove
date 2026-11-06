---
name: data-upserts
description: "Full overwrites waste the cluster and lose concurrent writes; lost watermarks drift forever."
---

# Merge by keys, never full overwrite

Create and install a skill named `data-upserts` (Merge by keys, never full overwrite). It instructs the agent as follows: Merge only new or changed rows by keys or watermarks — naive full overwrites waste the cluster and lose concurrent writes. Watermarks advance only after the merge commits; a crashed load resumes from the last committed mark, never from zero.

## Checks

- keyed merges, no full overwrites
- watermarks advance on commit
