# TODO — what still needs doing (from README)

## Setup

- [ ] Export `RESEND_API_KEY` so the contact dialog sends mail (without it the
  form shows "not set up yet" instead of sending).
- [ ] Verify the sending domain at `resend.com/domains` when moving off the
  `onboarding@resend.dev` test sender.
- [ ] Deploy the Worker mirror (`npx wrangler login` once, then
  `npx wrangler deploy`; pushes to `main` auto-deploy after that).

## Later (not now)

- [ ] **Redis** — shared store for the rate-limit buckets and the cache layer
  when the app outgrows one process (Upstash free tier).
- [ ] **Donations** — pick a platform (Ko-fi, Open Collective, GitHub
  Sponsors); it lands behind the existing `support us` button.
- [ ] **DevSecOps skills** (bank growth, not project tooling) — research
  secret scanning, dependency audit, gated deploys, signed artifacts as
  future skills; build them when the bank earns them.
