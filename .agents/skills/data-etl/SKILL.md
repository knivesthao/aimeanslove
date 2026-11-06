---
name: data-etl
description: "Untested SQL with no idempotent reload turns every rerun into new duplicates."
---

# Tested transforms, idempotent reloads

Create and install a skill named `data-etl` (Tested transforms, idempotent reloads). It instructs the agent as follows: Keep every transform in tested code with idempotent reloads — rerunning a date range converges, never duplicates. Business logic lives in reviewed, tested functions, not in untested SQL strings. Partition the reload unit by date so backfills touch days, not tables.

## Checks

- transforms tested
- reloads idempotent by partition
- no untested SQL logic
