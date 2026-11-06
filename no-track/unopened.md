# Sources not opened (yet)

Every item below is a real source we could not read in-session. URLs are kept
so a human can pull them later (like the JECI rescue). Nothing here is cited
anywhere until it is read.

## Paywalled or bot-blocked

- Healey (2007), "Drop Downs and Scroll Mice" full text — SAGE blocks bots
  (403). Abstract, APA record, and two independent citations verified the
  findings (higher item nonresponse, longer response times, accidental
  changes). Backlink uses the canonical DOI, which loads for humans.
  https://journals.sagepub.com/doi/10.1177/0894439306293888
- JECI ftp PDF mirror — 403 for bots. Superseded: the article page loads and
  was read in full. No action needed.
  https://ftp.academicjournals.org/journal/JECI/article-full-text-pdf/61BAE8470266
- Material Design token docs (m3.material.io) — JavaScript-rendered, fetch
  returned 33 characters. Token-layer concept taken from Fowler + USWDS
  instead (both read in full).
  https://m3.material.io/foundations/design-tokens/overview
- Apple Human Interface Guidelines — JavaScript-rendered, fetch returned 51
  characters. Radio/segmented guidance already covered by NN/g + Microsoft;
  not pursued further (diminishing returns).
  https://developer.apple.com/design/human-interface-guidelines/designing-for-macos

## Still missing — please supply

- The red/purple/blue traffic study (R² = 0.9912) from the original research
  batch. Not found anywhere; only generic color-psychology marketing pages
  exist. If you have the link or PDF, drop it in `docs/research/` (gitignored)
  and say the word. Until then the guide claims nothing from it.

## Evaluated and rejected (read, not used)

- AICSS (aicss.dev) — commercial component library (paid Pro, React/Vue/
  Svelte) for agent chat UIs. Rejected: paid plus React-first conflicts with
  the free, no-React stack. Revisit if the stack ever changes.
  https://www.aicss.dev/
- awesome-generative-ui (GitHub link list) — discovery only, no findings to
  extract. Not pursued.
  https://github.com/narrowin/awesome-generative-ui
- Radix Primitives — React-only component library. Rejected for the same
  reason as AICSS: our stack builds islands in Lit, not React.
  https://github.com/radix-ui/primitives
