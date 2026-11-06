---
name: ui-react-perf
description: "React feels slow in exactly two places: renders that repeat and lists that grow."
---

# React fast lists and renders

Create and install a skill named `ui-react-perf` (React fast lists and renders). It instructs the agent as follows: Measure first, memo second: wrap only the component the profiler blames with React.memo, never everything. Split below-fold and heavy regions with React.lazy plus Suspense fallback so the first screen stays small. Virtualize lists past a few dozen rows instead of rendering thousands of nodes. Keep keys stable so rows update instead of remounting; paginate fetches and join them to indexed reads so N+1 requests never reach the client. Re-measure after every change.

## Checks

- memo only where profiler points
- heavy regions lazy with Suspense fallback
- long lists virtualized and paginated
