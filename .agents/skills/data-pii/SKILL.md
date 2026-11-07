---
name: data-pii
description: "Retention rules on unlabeled data are theater; the PII lives in note_2."
---

# Find PII before you policy it

Create and install a skill named `data-pii` (Find PII before you policy it). It instructs the agent as follows: Classify before retaining: scan text fields, webhook payloads, and new columns for personal data on a schedule — PII hides in free text and oddly named columns. Label what you find at the source; retention and erasure act on labels, never on guesses. Quarantine unlabeled new sources until classified. Re-scan when producers change shape.

## Checks

- scheduled scans of text and new columns
- retention acts on labels
- unlabeled sources quarantined
