---
name: data-metrics
description: "Two dashboards with two definitions of revenue are both reproducible and both wrong."
---

# One definition per metric

Create and install a skill named `data-metrics` (One definition per metric). It instructs the agent as follows: Define each metric once, in one registry owned by one team: name, formula, inputs, and grain. Dashboards and models read definitions, never re-derive them. Flag duplicate names with different formulas as incidents. Changing a definition versions it; restating history replays from the new version with the change logged. Movement is agent work; meaning is decided by people, then written here.

## Checks

- each metric defined once with an owner
- duplicate names flagged as incidents
- definition changes versioned
