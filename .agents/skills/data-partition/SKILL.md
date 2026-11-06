---
name: data-partition
description: "High-cardinality partitions spawn thousands of tiny files that slow every reader."
---

# Prunable keys, no tiny files

Create and install a skill named `data-partition` (Prunable keys, no tiny files). It instructs the agent as follows: Partition by low-cardinality date or key so queries prune whole ranges. Never high-cardinality IDs — they spawn thousands of tiny files that slow every reader. Target files sized for the reader (tens to hundreds of MB); compact the small ones on a schedule.

## Checks

- prunable low-cardinality keys
- no tiny-file sprawl
- compaction scheduled
