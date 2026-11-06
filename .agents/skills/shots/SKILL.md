---
name: shots
description: Save verification screenshots to the project's shots/ folder (gitignored), never /tmp.
---

# Shots

When you screenshot a page to verify your work:

- Save into `<project>/shots/` (create it if missing), named for what it shows, e.g. `shots/board-mobile.png`.
- Make sure `shots/` is listed in the project's `.gitignore` so verification images never bloat commits.
- Never save screenshots to `/tmp` — hidden files pile up unseen and nobody can find them later.
- When you finish, delete scratch files you made in `/tmp`, and only those — never touch files another process owns.
