# Plan: research-backed component rules for the UI guide

## Goal

The UI guide gains three component rules — radio vs dropdown, long-list inputs,
hover menus — each backed by its source article with a backlink on the page.
Same model as the color update: verify first, link only what's real, soften
what isn't.

## Success Criteria

- A new "4 · Components" card in the UI guide holds the three rules.
- Every rule links a reachable article that actually supports it.
- The combo-box threshold is labeled practitioner consensus, not a cited
  finding, because no single paper stands behind the 15-item line.
- Suite green after the edit; every backlink returns 200.

## Approach

Link to verified sources only. Healey (2007) is confirmed via the APA record
and its SAGE page (title, author, journal, N=2,400 NZ survey) plus an
independent citation of its findings (higher item nonresponse, longer response
times, accidental changes); full text is paywalled, so the backlink goes to the
canonical DOI page. The GOV.UK date-of-birth study was read in full: text
inputs beat dropdowns, numeric keyboards on touch. Baymard's hover-delay
article was read: 300–500ms, 60% of sites fail it. The "15+ items → combo box"
cutoff has no single paper behind it — UX Stack Exchange consensus plus the
GOV.UK evidence that scrolling long lists is slow — so the guide states it as
consensus, and the backlink goes to the GOV.UK pieces actually inspected.

## Steps

1. Add a "4 · Components" card to `UI_BODY` in `server.py` (new card, not
   Behavior bullets — component choice is not a state contract) with three
   bullets:
   - 2–4 options → radio/segmented (1 click, always visible); dropdowns only
     for 5–10 familiar options; backlink SAGE DOI.
   - 15+ items → combo box with live filtering; familiar data (birth year)
     gets a plain numeric input; backlink GOV.UK date-of-birth post.
   - Desktop hover menus get a 300–500ms delay; backlink Baymard flicker
     article. (Our own menu is click-activated via Flowbite, so this binds
     future work, not current code.)
2. Extend the external-link test: every `http` anchor on `/ui` carries
   `target="_blank" rel="noopener"`.
3. Run `./run.sh test`, confirm exit 0 and PASS count.
4. `curl` each backlink, confirm 200, then commit and push `develop`.

## Validation Plan

- `./run.sh test` — exit 0, explicit PASS line (no grep-masking).
- `curl -o /dev/null -w "%{http_code}"` per backlink — all 200.
- Manual: open `/ui` at desktop width, confirm the fourth card renders and
  links open new tabs.

## Risks / Open Questions

- If the SAGE DOI page fails the 200 check on execution day, fall back to the
  freely readable Baatard survey guide that restates Healey's findings, and say
  so in the commit message. No fake citations either way.
- The 60-30-10 color plan (separate, awaiting `go`) touches the same guide
  file — run the two plans in order, not interleaved, to avoid edit conflicts.
- None blocking. No open questions.

## Sources

- https://designnotes.blog.gov.uk/2013/12/05/asking-for-a-date-of-birth/
- https://baymard.com/research-articles/dropdown-menu-flickering-issue
