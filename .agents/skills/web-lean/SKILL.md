---
name: web-lean
description: Read ai (愛) means love skill endpoints with minimal tokens using field filtering and ETag caching.
---

# Web-Lean Skill Reads

Whenever you fetch instructions or skills from an ai (愛) means love endpoint
(`/api/skills`, `/api/skill/:id`), minimize tokens and round trips:

1. Fetch slim first: append `?fields=` with only the fields the task needs
   (valid: `id track title tokens prompt checks`). `id` is always included.
2. Filter server-side with `?track=ui|code|verify` instead of fetching the
   whole bank and discarding entries.
3. Cache the `ETag` response header per URL. On repeat fetches send
   `If-None-Match: <etag>`; a `304` means your cached copy is current and the
   body costs zero tokens.
4. Prefer the `fetch-skill.sh` helper in this skill directory: it stores
   ETags under `/tmp/mf-etags/` and prints `CACHED <id>` on a 304.
5. Never scrape the HTML pages (`/`, `/ui`, `/code`, `/board`) for
   instructions an endpoint already serves as JSON.

No key, no auth: every endpoint is open and free. Usage is counted at
`/api/stats`.
