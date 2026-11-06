---
name: code-notify
description: "Blocking inline sends turn every retry into a double-notify and every surge into a timeout."
---

# Queued templated sends, never blocking

Create and install a skill named `code-notify` (Queued templated sends, never blocking). It instructs the agent as follows: Send every notification through a queue with a template — never blocking inline sends. Each user holds channel preferences (in-app, email, SMS, push); respect quiet hours with digested batches. Dedupe on event keys so retries never double-notify. Every outbound message carries a working unsubscribe; marketing and transactional never share a path.

## Checks

- queued templated sends only
- dedupe keys, no double-notify
- working unsubscribe
