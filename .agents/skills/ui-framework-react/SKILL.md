---
name: ui-framework-react
description: "React scales by splitting server from client at the file boundary — one directive decides where code runs."
---

# React: server-first components

Create and install a skill named `ui-framework-react` (React: server-first components). It instructs the agent as follows: Build with small components — one job each, state colocated with the UI that uses it, stable keys on every list, no manual DOM writes (refs are the escape hatch, not the tool). Server-first where the setup allows (Next.js App Router): fetch and render on the server, mark only interactive files with 'use client'. Plain client-only React can't do server-first — same rules, no server. Style with className plus your pipeline's CSS; keep ready-made pieces from a stocked library instead of hand-built dropdowns and dialogs. Apply the generic component rules too (see ui-framework).

## Checks

- state colocated, lists keyed
- 'use client' only where interactive
- no manual DOM writes
