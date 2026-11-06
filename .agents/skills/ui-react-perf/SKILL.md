---
name: ui-react-perf
description: "Two thresholds — memo only the blamed component, virtualize past a few dozen rows."
---

# React fast lists and renders

Create and install a skill named `ui-react-perf` (React fast lists and renders). It instructs the agent as follows: Wrap only the component the profiler blames with React.memo, never everything. Split below-fold and heavy regions with React.lazy plus Suspense fallback. Virtualize lists past a few dozen rows. Paginate fetches so N+1 requests never reach the client.

## Checks

- memo only where profiler points
- heavy regions lazy with Suspense fallback
- long lists virtualized and paginated
