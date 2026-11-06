---
name: code-logging
description: "You can't respond to an attack you never recorded or never noticed."
---

# Logs that catch break-ins

Create and install a skill named `code-logging` (Logs that catch break-ins). It instructs the agent as follows: Log the events that catch break-ins: failed logins, validation failures, permission denials, and spikes in costly endpoints. Keep logs structured (who, what, when) and secret-free — logs get copied and shared. Watch them with an alert, not just storage: an unread log is decoration.

## Checks

- auth and deny events logged
- no secrets in logs
- alerts on spikes, not just storage
