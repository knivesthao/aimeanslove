---
name: code-impexp
description: "Synchronous bulk queries time out, and one bad row should not kill the file."
---

# Bulk moves as background jobs

Create and install a skill named `code-impexp` (Bulk moves as background jobs). It instructs the agent as follows: Run every bulk import and export as a background job with progress — never a synchronous request that times out. Validate encoding and schema row by row, quarantining bad rows instead of failing the file. Page reads in bounded batches; the export that loads the whole table is the outage. Notify on completion with the error report attached.

## Checks

- background jobs with progress
- bad rows quarantined, not fatal
- bounded batches
