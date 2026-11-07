---
name: data-quality
description: "Row counts pass plausible-but-wrong data; the bad numbers ship to every dashboard."
---

# Gate promotion on signals, not row counts

Create and install a skill named `data-quality` (Gate promotion on signals, not row counts). It instructs the agent as follows: Gate every promotion on freshness, nulls, volume, and distribution — row counts alone pass plausible-but-wrong data. Failing checks block the pipeline and page the dataset owner, with the offending sample attached. Track quality history per dataset; page only on shifts that name an owner and an action — alert fatigue trains teams to ignore every page, including real ones.

## Checks

- multi-signal gates, not row counts
- failures block with samples
- quality history tracked
