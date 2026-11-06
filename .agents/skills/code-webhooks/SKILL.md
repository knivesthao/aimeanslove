---
name: code-webhooks
description: "Unsigned fire-and-forget posts leave customers debugging your deliveries with no tools."
---

# Signed payloads with replay

Create and install a skill named `code-webhooks` (Signed payloads with replay). It instructs the agent as follows: Sign every outbound payload so receivers can verify it; version the event schema. Retry with backoff on failure and keep a delivery log per destination with replay — customers debug with replays, not with your logs. Receivers dedup on event ids, so sending twice is safe. Never fire-and-forget.

## Checks

- signed versioned payloads
- retry plus replay per destination
- delivery logs customer-visible
