# ai (愛) means love

Tooling so AI agents build faster with fewer tokens. Human-readable code is a token tax — this project writes code for agents to read cheaply, and humans verify only two things: **tests pass** and **the UI looks right**.

Free-tier stack: FastAPI + Pydantic server, Cloudflare Workers mirror (no paid bindings). Local dev needs Python 3.12+.

## Run

```bash
./run.sh dev   # sets up .venv on first run, uvicorn auto-reloads on edits
# → http://localhost:8787 — open that URL in a browser
```

Stop it with `Ctrl+C` — it runs in the foreground, so stopping is just interrupting it. Start again with the same command.

## Test

```bash
./run.sh test  # open endpoints + usage stats, stdlib only
```

## Pages (humans) / endpoints (agents)

| Route | For |
|---|---|
| `/` | Manifesto (home) |
| `/code` | Coding guide (Python first, guardrails) |
| `/ui` | UI styling + behavior guide |
| `/board` | Skill memory bank (filter + copy) |
| `GET /llms.txt` | Agent sitemap |
| `GET /board.json` | Full bank preview |
| `GET /api/skills[?track=][&fields=id,prompt]` | Whole bank, ETag-cached |
| `GET /api/skill/:id[?fields=prompt,checks]` | One skill (~100–170 tokens slim), ETag-cached |
| `GET /api/fields` | List of filterable field names |
| `GET /api/stats` | Usage counts: requests, per-route, per-skill |

No keys. Everything is open and free; usage is counted at `/api/stats`.

Token badges come from a test we ran on ourselves: `cl100k` tokenization over the exact JSON our own endpoints serve. Exact counts vary by model, so badges stay approximate (`~`).

## Contact form (dialog + Resend)

Every page has a `contact us` pill that opens a native `<dialog>` with the contact
form. It posts to `POST /contact` (plain form post, no JS needed). The server
validates `name` / `email` / `message`, drops bot posts via a `company`
honeypot field, and sends the email through Resend.

Setup (optional — without a key the form shows a "not set up yet" note instead
of crashing):

```bash
export RESEND_API_KEY=re_...          # free tier is enough
export CONTACT_TO=knives.thao@gmail.com  # default already
```

Verify `resend.com/domains` for your sending domain if you move off the
`onboarding@resend.dev` test sender.

## Deploy (free)

```bash
npx wrangler login
npx wrangler deploy
```
