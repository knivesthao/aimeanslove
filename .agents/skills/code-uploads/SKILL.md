---
name: code-uploads
description: "Files through the app server bottleneck it; filenames lie; public buckets leak."
---

# Direct-to-storage, private by default

Create and install a skill named `code-uploads` (Direct-to-storage, private by default). It instructs the agent as follows: Upload straight to storage with signed URLs — files never transit the app server. Trust MIME by content sniffing, never the filename; cap sizes at the edge. Scan asynchronously and quarantine on hit; serve everything private by default through signed URLs, never public buckets.

## Checks

- direct-to-storage signed URLs
- MIME sniffed, sizes capped
- private by default
