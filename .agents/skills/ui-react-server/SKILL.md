---
name: ui-react-server
description: "Server components move fetching off the phone — one directive decides where code runs."
---

# React server-first with Next.js

Create and install a skill named `ui-react-server` (React server-first with Next.js). It instructs the agent as follows: Standalone React (Vite, CRA, no App Router)? Stop — skip this skill and read ui-react-components plus ui-react-hooks instead. Next.js App Router only: fetch and render on the server by default — async server components own the data, props carry only serializable results to the client. Mark only interactive files with 'use client' — typing, dragging, live state — and keep server secrets out of them. Give each route loading.tsx and error.tsx so waiting and failure are designed states, not blank screens.

## Checks

- standalone setups skip this skill
- data fetched on the server where allowed
- 'use client' only where interactive
- loading and error states designed
