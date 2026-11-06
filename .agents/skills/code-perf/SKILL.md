---
name: code-perf
description: "Users feel milliseconds and megabytes; everything else is invisible."
---

# Fast by budget

Create and install a skill named `code-perf` (Fast by budget). It instructs the agent as follows: Set a budget first: page weight, endpoint milliseconds, query count — then measure before changing anything. Cache first (see code-cache): repeated work should never recompute. Shrink the payload: paginate lists, select only needed columns, compress images, ship less JavaScript. Push heavy work out of the request into background jobs, and turn N+1 reads into single joined or batched reads on indexed columns. Re-measure after every change; speed you can't see is a guess.

## Checks

- budgets set before optimizing
- repeat work cached, not recomputed
- N+1 reads batched or joined
