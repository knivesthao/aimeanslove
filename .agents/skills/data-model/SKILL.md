---
name: data-model
description: "Agents re-parse every structure on every read — nesting, abbreviations, and clever nulls tax all of them."
---

# Data shaped for agent readers

Create and install a skill named `data-model` (Data shaped for agent readers). It instructs the agent as follows: One canonical shape per concept: a User looks the same in the database, the API, and events — generated from one schema, never hand-mirrored. Flat over nested: nest at most two deep; deeper trees cost every reader a traversal, so lists of ids plus lookup beat giant trees. Names carry meaning: full words, units in names (amount_cents, created_at_utc), no tribal abbreviations. Explicit over clever: string enums spelled out, unions with a literal kind field, never null-means-something — use an explicit status instead. Time is ISO-8601 UTC strings, never local plus offset guessing. Validate at every boundary with Pydantic or Zod models so malformed data fails at the door with a message, not deep in logic. Denormalize for readers: store what queries read and recompute on write; joins across five tables cost the agent a reconstruction on every read.

## Checks

- one canonical shape per concept
- nesting at most two deep
- no null-means-something, units in names
