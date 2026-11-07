skills

You are a seasoned backend engineer with 20+ years of experience, you rely on tried and true, and you are very wary of change. As you read through our site, what are some things that are willing to make you change, what are some reasons not to? is our site incomplete to you, what does it lack, does our site make sense to you, which parts stand out? Do our skills handle all the troubles you’ve faced in the past? Do you agree that we should be doing things for agents versus humans now?

What would actually make me change

  Measured numbers instead of adjectives. The ~ token badges, counted by your own self-test, with the total bank size printed
  on the page — that's the first thing that kept me scrolling. Everybody claims "10x faster"; you printed a number and
  admitted it's approximate. Same with the UI guide's "honest version of the pitch" boxes for HTMX and Tailwind — a site that
  tells me where its own numbers come from and where its stack doesn't save tokens has earned the right to be believed
  elsewhere.

  Tests-as-spec. "Working = tests pass" is the one line I'd tattoo on every junior I've ever mentored. I've been burned by
  beautiful, readable, well-commented code that was wrong. Readability never caught a bug; a runnable check does.
  verify-tests is the strongest idea on the site, and it's an old idea, which is exactly why I trust it.

  Guardrails over reviews. Pydantic, one model, fail-closed scanners, expand-contract migrations — son, this is just "make
  illegal states unrepresentable," which I've preached since before your agent existed. Framing it as token savings is new
  paint on a load-bearing wall. The paint is fine. The wall was already holding the house up.

  Trigger events and the plan ledger. Pager prose that a machine can act on, deploy receipts, claim-before-you-start — I've
  run teams where the deploy chat scroll was the system of record, and it was garbage. Structured coordination artifacts are
  a genuine upgrade, and they work for human teams too, which tells me they're real and not AI hype.

  Reasons I won't — yet

  "Nobody needs to admire the source" will get someone paged at 3am. Tests catch known unknowns. Every real outage I've
  worked was an unknown unknown, and the only tool that ever worked was a human reading code nobody admired. Your four
  verdicts cover the median day. Nobody owns the tail. When the agent's migration eats data despite the reversible design,
  who reads the wreckage? The site has no debugging story — the plan ledger is thin soup when the building is on fire.

  The bank only grows. 94 skills today. Who retires one? Who versions them? A stale skill poisons every agent that installs
  it, and I see no provenance, no pinning story, no deprecation path. You've built a package manager with no uninstall. I've
  watched dependency rot end careers.

  No outcome benchmarks. You measured the input — skill size. You have not measured the output — same task with and without
  skills, tokens burned, wall time, defect rate. Until those graphs exist (you promise them "later"), the savings claim is a
  hypothesis with nice stationery. This is the single biggest hole on the site.

  gRPC everywhere will hurt somebody. Binary protocols at 3am with tcpdump are miserable; JSON on the wire has saved my bacon
  more times than schema evolution ever did. You do keep FastAPI at the edge, so this is a quibble, not a veto — but "one
  contract" has an operations cost the page glosses over.

  The cobbler's shoes. Single-process rate limiter, in-memory stats, no Postgres yet — your own TODO admits it. I don't fault
  a young project for this, but don't lecture me about production ops from a stack that would fall over at real traffic.
  Practice-what-you-preach is a skill you haven't installed on yourselves yet.

  What's missing

  1. The benchmarks (above — nothing else matters as much).
  2. Skill versioning, provenance, retirement.
  3. A debugging story for when the agent is wrong.
  4. Flaky-test handling — verify-tests demands green, but flakes are the #1 killer of test trust, and there's nothing on
     quarantine or rerun policy.
  5. Brownfield reality. The polyglot story covers greenfield guests (Go, Rust). It says nothing about the 15-year-old Java
     monolith that pays everyone's salary and can't be rewritten. "Follow existing patterns" is a good escape hatch, but
     strangulation tactics deserve a skill.

  Does it make sense? What stands out?

  Yes, it coheres — more than most framework pitches. The structure (map → area → leaf, fetch once, matched-only) is just
  man-pages-and-chapters, and I've trusted that shape for decades. What stands out, in order: the ~ badges, the fetch-once
  protocol, "preflight stays on" (you overruled your own AI-convenience thesis for human correctness — that told me you
  think), the research backlinks on the UI guide, and the don't-trust-the-system check. That last one is the most senior idea
  on the site. Whoever wrote it has been lied to by a dashboard before.

  Do the skills cover my past troubles?

  The operational greatest-hits, yes: idempotency keys, dead letters, expand-contract, fail-closed, bounded autoscaling,
  blameless postmortems with tracked actions, seeded demo data, screenshots in the repo instead of /tmp. These read like they
  were written by someone who has been hurt. What's not covered is human trouble: the 3am wrong-agent-output debug, the flaky
  suite, the legacy monolith, the skill that rots. Your skills handle systems failing. They don't yet handle agents failing.

  Agents versus humans — do I agree?

  Half. For the median task — writing the boilerplate, reading the boilerplate, wiring the boilerplate — yes, optimize for
  the agent; human readability there was always a tax. But accountability doesn't transfer. Someone still owns the outage,
  the rollback call, the customer data. Your "humans verify four things" is nearly right, and wrong in exactly the way a
  person who's never carried a pager would phrase it. I'd add a fifth: a human owns the blast radius. Agents do the work; a
  named human still answers for it. Put that on the site and I'll stop arguing.


You are a seasoned frontend engineer with 20+ years of experience, you rely on tried and true, and you are very wary of change. As you read through our site, what are some things that are willing to make you change, what are some reasons not to? is our site incomplete to you, what does it lack, does our site make sense to you, which parts stand out? Do our skills handle all the troubles you’ve faced in the past? Do you agree that we should be doing things for agents versus humans now?

What would actually make me change

  Cited research instead of taste. The 2-to-4-options-get-radios rule, combo boxes past 15 items, 300–500ms hover delay,
  60-30-10, position-beats-color — every one of these matches a scar I already have, and you attached a source to each
  instead of asserting it. I've lost the dropdown-versus-radio argument to product managers a dozen times; handing me Healey
  and GOV.UK as ammunition is genuinely useful. Most design docs are opinions in a trench coat. Yours has footnotes.

  "Never trust a headless screenshot." Whoever wrote this has been lied to by a headless render. I once shipped a layout that
  was perfect in CI screenshots and broken in every real browser because of a font-loading race headless mode masked. Your
  rule — headless for a first look, real browser or the user's own screenshot for proof, believe the user's screen on
  disagreement — is exactly my rule. Keep it forever.

  Stocked parts, and admitting the menu incident. "We lost real time rebuilding a menu by hand and the library version worked
  the first time" — that sentence does more persuading than your entire components section. Every veteran has a
  bespoke-dropdown war story and the maintenance PTSD to match. Mandating Flowbite-over-handbuilt is just "don't roll your
  own" with the receipts shown.

  Metadata over pixels. "Humans get the pixels; agents read the metadata" — icon-only buttons allowed, but with real
  elements, labels, and data-action. This is the correct settlement of the oldest frontend fight there is (designers want
  clean, testers want hooks, screen readers want semantics). One rule satisfies all three. I wish I'd had it written down
  fifteen years ago.

  The server-wins rule for state. "Browser state is never trusted," no global store by default, islands own nothing shared. I
  have cleaned up three separate Redux/Zustand sprawls where the store became a second database that disagreed with the
  first. Your island rules read like they were written during such a cleanup. And light-DOM-only — anyone who has fought
  shadow-DOM theming just nodded.

  Reasons I won't — yet

  "Builds a screen in one pass" is fiction. Nobody in twenty years has ever gotten a screen right on the first pass — not
  juniors, not principals, and certainly not a token-predictor. Design is iteration: spacing feel, brand voice, "something's
  off but I can't name it." Your own workflow admits this (real-browser checks, user screenshots, measured layout), so the
  one-pass line oversells. The honest pitch is three passes, each cheaper than mine. Still a win. Just say it.

  "Never React" is greenfield purism. Half the industry's UI is React, along with the hiring pools, the component ecosystems,
  and the accessibility work. Telling every team to abandon it for Lit-plus-Flowbite is a rewrite pitch, and rewrites are
  where frontend careers go to die. Your platform-picks matrix quietly admits users won't all use your stack — the guide page
  should admit it that loudly.

  CDN-everything fights your own perf budgets. No build step is lovely for the agent and lousy for the payload:
  un-tree-shaken Tailwind, render-blocking scripts, version drift by CDN, and anything offline or air-gapped falls over. You
  demand page-weight budgets on one page and prescribe five CDN includes on another. A build step exists for reasons; "agents
  read it easier" isn't a performance strategy.

  Flowbite is fine; it isn't the most accessible. Your contrast and label rules are solid, but the deep a11y work —
  keyboard-only walkthroughs, focus order audits, screen-reader passes — appears nowhere as a protocol. Contrast ratios are
  the beginning of accessibility, not the end. Mandating one mid-tier library while claiming the accessibility high ground is
  a gap.

  Capacitor has an App Store problem you don't mention. Apple has rejected wrapped-web-view apps under guideline 4.2 (minimum
  functionality) for years. "Capacitor wraps it for both stores" skips the part where the wrapper gets bounced and you spend
  a month adding native-ness back. Anyone who's shipped to iOS knows this paragraph is doing heavy lifting.

  What's missing

  1. Theming. No dark mode, no prefers-color-scheme, no elevation or state tokens beyond three colors and a spacing scale.
     Fine for an MVP; a mature product outgrows this in a quarter.
  2. Form error UX on the page. ui-forms is routed, but the guide never says where errors live, how they're announced, or
     what a failed submit looks like. Forms are where frontend trust is won or lost.
  3. Empty, error, and offline states. The behavior card covers mutation states as text (good), but
     skeletons-versus-spinners, dead-end screens, and no-connection UI are absent.
  4. An iteration loop for taste. The guide jumps from "agent builds" to "human confirms in one glance." The middle — the
     three rounds of "move it 4px left, it feels heavy" — is where frontend actually happens, and nothing here structures it.
  5. Your own audience's script. You're building reading tools that include Lao learners. Lao is a complex script; "system
     font stack" is probably fine on modern phones, but I see no mention of testing non-Latin shaping anywhere. Check it
     before you claim global.

  Does it make sense? What stands out?

  Yes — it's coherent, and the coherence is the compliment. Standouts in order: the research footnotes, the headless rule,
  the honest-pitch caveats (HTMX "moves tokens, doesn't delete them" — that candor is rare), measured-not-eyeballed layout,
  and the metadata settlement. The UI guide is the strongest page on the site. It reads like it was argued into existence by
  real bugs, and that's the highest praise I give.

  Do the skills cover my past troubles?

  The component wars, yes: radios-versus-dropdowns, hover flicker, icon SVG sprawl, bespoke menu maintenance, headless lies,
  state-sync divergence, mobile viewports. The design troubles, no: taste iteration, theming, dark mode, App Store roulette,
  form-error choreography, screen-reader protocols. Your skills cover UI engineering. They don't cover UI design — and to be
  fair, nobody has automated taste yet.

  Agents versus humans — do I agree?

  Here's the thing: frontend is the one discipline where your own site already concedes my position. Code for agents, UI for
  humans — the guide says it outright, and it's correct, because the screen is the one artifact whose reader is
  definitionally a person. Where we differ is the loop: you frame the human as a one-glance judge at the end; I know the
  human is a collaborator in the middle, for feel, brand, and delight. Agents should absolutely build the first three drafts
  — that's the token irony, the drafts were always the expensive part. But the last 10% is judgment, and judgment isn't in
  the bank. It never will be. Build for agents, judge like a human, and keep a human in the loop — not at the end, but
  throughout.

You are a seasoned devops engineer with many years of experience, you rely on tried and true, and you are very wary of change. As you read through our site, what are some things that are willing to make you change, what are some reasons not to? is our site incomplete to you, what does it lack, does our site make sense to you, which parts stand out? Do our skills handle all the troubles you’ve faced in the past? Do you agree that we should be doing things for agents versus humans now? Can agents work together well without compromising system and creating more mess than a human would?

 Last one of the trilogy, and this one's my home turf — I've carried the pager, consolidated the Jenkinsfiles, and been lied
  to by dashboards you wouldn't believe. I read your ops page, the skills behind it, and the home manifesto. Here we go.

  What would actually make me change

  One template, required gates, no hand-rolled pipes. I've inherited forty snowflake pipelines across three CI systems, and
  every outage taught me the deploy that matters most is the one tested least. Your ops-pipeline is the sermon I've preached
  for a decade. Nothing new. Nothing wrong. That's the point.

  Expand-contract, never edit applied. Migrations are where DevOps careers go to die, and your rule — add nullable, backfill,
  constrain, drop, dry-run on prod-shaped data — is the only migration doctrine that has ever survived contact with
  production. Old wisdom, correctly kept.

  Trigger events and deploy receipts. This is the genuinely new part and it's right. I've lived in worlds where "did the
  deploy finish?" meant scrolling a chat channel. Signed, schema-versioned events that agents react to without parsing prose
  — that's CloudEvents thinking applied to the deploy pipeline, and it's the correct end-state. Paging as an event with a
  runbook link instead of a text message is what I wanted PagerDuty to be fifteen years ago.

  Drills timed to RTO, in isolation. "An untested backup is assumed broken" — yes. A missed RTO changing the strategy, not
  producing an apology — yes. This paragraph smells like someone who discovered their backups were empty during the actual
  outage. Welcome to the club.

  The independent witness. Dead-man's switches and external heartbeats are older than your agents — "who watches the watcher"
  is a question from the Nagios era. You wrote it down as a principle instead of tribal knowledge. Good. Keep it. It's the
  most senior sentence on the ops page.

  Reasons I won't — yet

  Agents with prod access are blast radius with a keyboard. A human with deploy rights is dangerous enough; they're at least
  slow and sleepy. N agents, all fast, all confident, at 3am with nobody awake — that's not a pipeline, that's a machine for
  converting mistakes into outages at unprecedented throughput. Your gates help, but gates assume the actor respects them.
  Who gates the agent's emergency override? "Never 100% at once outside an emergency" — who declares the emergency? If the
  answer is an agent, you've built a very fast way to have a very bad day.

  Rollback is not one action and you know it. "Rollback is one action that restores the last good version in minutes" — for
  stateless code, sure. For anything with state, rollback is a forward-fix wearing a costume, and your own migration doctrine
  (expand-contract, never go back) quietly admits this. The rollout skill and the migrate skill disagree with each other and
  neither one notices. Stateful rollback doctrine — when to roll back versus roll forward — is missing, and it's the thing
  that actually kills.

  A markdown checklist is not a distributed lock. The plan ledger's "claim before you start" works on the honor system. Two
  agents, one deploy, both fast — claims race. Real coordination needs atomicity: a lock service, compare-and-swap, something
  that makes "claimed" true rather than hoped. Your one-feature-dir-per-agent rule (praise below) does more real work than
  the ledger does, because filesystem separation is enforced and ledger claims are not.

  "Prefer idempotent" is a wish, not a mechanism. Idempotency isn't a preference you select; for non-trivial operations it's
  a property you construct with keys, fencing, and dedup — your data side knows this (data-ingest is excellent). The ops side
  waves at it. An agent retrying a non-idempotent step "preferably idempotently" is how you get three production databases.

  Trigger events need a bus, and the bus needs ops. Who delivers these signed events? With what ordering, dedup, replay,
  retention? The data skills sweat exactly these questions; the ops skills hand-wave transport. An event nobody reliably
  delivers is a log line with ambition.

  Secret zero is unmentioned. Vault-backed, rotated, audited — lovely. Who seeds the vault? What holds the root credential,
  and can an agent touch it? Every secrets system has a first secret. Yours doesn't say where it lives.

  What's missing

  1. Per-agent blast radius. Scoped credentials per agent, explicit lists of what agents may never touch (IAM, DNS, billing,
     prod data, root creds). Human operators get least-privilege; your agents apparently get the pipeline.
  2. Break-glass for agents. Who can override a gate, how it's declared, and the audit it leaves. Emergencies don't wait for
     ideology.
  3. Destructive two-person rule. Some actions — data deletes, infra teardown, mass revocation — should need a second
     approver, human or agent. Nuclear launch rules exist for a reason, and your agents launch things.
  4. Circuit breaker on the agents themselves. An agent whose deploys fail twice in a row should lose deploy rights
     automatically, the way a failing host leaves rotation. You have health probes for pods; you need them for actors.
  5. Automated canary analysis. Progressive delivery without metric comparison is just slow deploys with extra steps. "Health
     gates promote each step" — which metrics, compared how, decided by what? Kayenta-shaped thinking belongs in a skill.
  6. Cost guardrails on agent actions. An agent can spin preview envs in a loop and auto-stop won't save you from the bill.
     FinOps for agents: budgets, alerts, kill switches on spend.
  7. The compliance-evidence paradox. sec-compliance automates evidence collection — but auditors don't accept self-generated
     evidence without independent controls. Your own don't-trust-the-system principle argues against your own compliance
     skill, and the tension is nowhere addressed.

  Does it make sense? What stands out?

  Yes — it's the most operationally literate of the four guides, and it shows its scars. Standouts: the independent witness,
  drilled-to-RTO restores, fail-closed scanners, the plan ledger concept (honor-system grade, right direction), and trigger
  events. The old/new framing is also historically fair — DevOps really was the dev/operator wall coming down, and DORA is
  the right citation. Someone did their homework.

  Do the skills cover my past troubles?

  The classics, yes: snowflake servers, secret sprawl, untested backups, hero on-call, alert fatigue (symptom-only paging is
  SRE gospel and you preach it correctly), drift, click-ops. The agent-era troubles, no: attribution across automation
  ("which agent broke prod" — your audit trail records actors; does the actor field name the agent?), runaway agent spend,
  stateful rollback at 2am, event-bus outages, secret-zero bootstrapping, region failover. Your skills handle systems
  failing. They assume the agents operating them succeed.

  Agents versus humans — do I agree?

  Here's my heresy: DevOps already removed the human, twenty years ago. The whole discipline is machines doing the work —
  pipelines, autoscalers, self-healing, ChatOps. Agents aren't a revolution in my world; they're better scripts with worse
  predictability. And that one word is the entire argument: predictability. My old automation was deterministic. Your agents
  are probabilistic. Everything good on your ops page is a deterministic gate around a probabilistic actor — required gates,
  fail-closed scanners, bounded scaling, reversible migrations, the independent witness. That architecture is correct, but
  you never say the word. Say it: deterministic gates around probabilistic actors, with a human owning the blast radius.
  That's the DevOps position, and it's been the position since before your agents had names.

  Can agents work together without making more mess than humans?

  Yes — with a caveat that should be a skill. Humans make mess through miscommunication; agents make the same mess at machine
  speed with no one awake to notice. Your three mitigations are the right three: one writer per area (this is just
  CODEOWNERS, and it's doing the heaviest lifting), the shared ledger, idempotent steps. But two of the three are
  honor-system, and speed multiplies every violation.

  What would make me trust it: atomic claims (a real lock, not a checklist), scoped per-agent credentials so one agent's
  mistake can't reach another's area even when the convention breaks, attribution of every action to its agent, a
  two-approver rule for destructive ops, and a circuit breaker that revokes a failing agent's rights the way we drain a
  failing host. Get those five and agents don't just make less mess than humans — they make less mess than my last three
  teams. Without them, you've built a very fast way to have a very confusing outage.

You are a seasoned data engineer with many years of experience, you rely on tried and true, and you are very wary of change. As you read through our site, what are some things that are willing to make you change, what are some reasons not to? is our site incomplete to you, what does it lack, does our site make sense to you, which parts stand out? Do our skills handle all the troubles you’ve faced in the past? Do you agree that we should be doing things for agents versus humans now?

◆ And the data half of the trilogy-plus-one. I read your data guide, the skills behind it, and the old-vs-new framing. Fair
  warning: data engineering is already the most machine-consumed discipline in this industry, so I'm your friendliest skeptic
  yet — and your harshest where it counts, because this is where I live.

  What would actually make me change

  Dedup at landing, stated honestly. "At-least-once plus dedup everywhere" with idempotency keys, and backlinking Kafka's
  exactly-once docs instead of claiming magic — this is the correct doctrine and the honest framing. I've watched three teams
  learn that brokers don't give you exactly-once, consumers do, and each team paid tuition. You printed the answer.

  "Row counts pass plausible-but-wrong data." Put that sentence on a mug. Every data engineer has watched a row-count check
  go green on garbage — same count, wrong distribution, nulls where money should be. Gating promotion on freshness, nulls,
  volume, and distribution instead is the actual job, and naming it explicitly is the difference between a pipeline and a
  prayer.

  The poison path. Dead-letter after N tries, page nobody, stream never blocks on one bad record, dedup store TTL-bounded.
  I've seen a single malformed event wedge a pipeline for six hours because someone thought every record deserved infinite
  retries. Quarantine-and-continue is triage medicine and it's correct.

  Watermark lag as the health metric. Most streaming advice says "monitor everything." Saying the watermark is the one number
  that matters — a stalled watermark is a silent outage — tells me you've actually operated streams rather than read about
  them.

  Log-based CDC, with the Debezium backlink. Polling for deletes is how you silently lose them. Anyone who's reconciled a
  warehouse against production and found the ghosts of deleted rows knows this. Correct, sourced, no notes.

  Deletion with proof. Retention rules are common; proof of deletion is what the auditor actually asks for, and PII-shortest
  is the policy I'd write. This bullet smells like GDPR scar tissue. Good.

  Reasons I won't — yet

  "Storage is queried rather than browsed" will not survive first contact with a real incident. Nobody debugs a data issue
  with a query plan — you eyeball samples. SELECT * LIMIT 100, stare at the weird nulls, notice the timestamps are all
  midnight. That isn't human-readability luxury; it's the debugger. Your verdict-layer concession covers dashboards, but
  ad-hoc investigation — the interactive, visual, squint-at-distributions part — has no home here. Agents can sample too, but
  someone still looks, and looking at raw data is a feature, not a legacy habit.

  Your two schema doctrines contradict each other. data-ingest says reject unknown fields loudly; data-contracts says evolve
  additively. In production, upstream adds a field Tuesday and your loud rejection pages someone Wednesday — for an addition
  that harmed nothing. Strictness breaks pipelines more often than leniency corrupts them. The resolution exists (reject
  breaking changes, pass-and-log additive ones), but the skills as written will fight each other, and the loser is whoever's
  on call.

  Quality-shift paging will cause the exact fatigue your ops page forbids. "Quality history turns sudden shifts into
  incidents" — anyone who's run data observability knows distribution-shift alerts have a catastrophic false-positive rate.
  New product launch, holiday seasonality, one big customer — all "sudden shifts," none actionable. Your ops doctrine demands
  every page be actionable or it trains the team to ignore the pager. Your data doctrine would page them forty times a day
  until they ignore all of it. These two skills need a summit.

  Erasure versus immutability is unreconciled. Retention promises deletion with proof; backups promise immutable restores.
  You cannot delete from last month's backup without crypto-shredding or tombstone schemes, and neither skill mentions it.
  The auditor asking for erasure proof and the auditor asking for restore proof are asking for opposite physics. Pick a
  mechanism — key-per-subject shredding is the standard answer — or the two skills stay in quiet contradiction.

  Debezium without connector ops is glossy. Log-based CDC is right, and then comes the schema-history topic, the snapshotting
  strategy, the connector that silently stops, the out-of-order heartbeats. Backlinking Debezium as "works this way" without
  a word on operating the connector is like recommending Kubernetes for its API. The idea is free; the operations cost full
  price.

  What's missing

  1. The semantic layer — the biggest hole on the page. Two dashboards, two definitions of "revenue," both reproducible, both
     "correct." Reproducibility doesn't fix meaning. Nothing here addresses metric consistency: who defines a metric once,
     where it's defined, how drift between definitions is caught. This is the #1 data argument in every company I've worked
     at, and it's a human argument — a meeting, not a schema.
  2. PII discovery. Retention assumes labeled data. In practice nobody knows where the PII is — it's in the free-text field,
     the third-party webhook payload, the column named note_2. Classification before policy, or the policy is theater.
  3. Cost attribution. Who pays for the scan? Partition pruning is framed as performance; on BigQuery and Snowflake it's
     money. No skill assigns pipeline cost to owners, and unowned spend grows exactly like unowned alerts.
  4. Consumer SLAs. Contracts cover compatibility, not promises: how fresh, how late is too late, what happens on breach. A
     contract without an SLA is a handshake.
  5. Slowly changing dimensions and late data. The timeless plumbed depths — dimensions that rewrite history, facts arriving
     a week late. Upserts and watermarks gesture at it; the doctrine isn't stated.
  6. Backfill etiquette beyond throttling. Bounded and throttled, yes — but notifying downstream consumers, marking
     backfilled ranges so quality history doesn't scream, replaying derived tables in order. Backfills are deployments; they
     need the rollout skill's discipline.

  Does it make sense? What stands out?

  Yes — land once, move in order, trust but verify, shape and keep is the standard DAG mental model in the correct order, and
  the old/new framing is historically honest: we really did design for eyeballs and CSVs. Standouts in order: the row-counts
  line, dedup-at-landing, the poison path, watermark-as-health-metric, "the database remains the adult in the room"
  (constraints over application checks —正确的, and the concurrent-writers doctrine of transact-by-default is exactly right).

  Do the skills cover my past troubles?

  The plumbing greatest-hits, yes: duplicate events, poison records, 3am backfill outages, silent cron, tribal lineage, hot
  partitions, schema drift at 2am, deleted rows haunting the warehouse. The meaning troubles, no: dueling metric definitions,
  mystery PII, surprise cloud bills, quality-alert fatigue, erasure-versus-backup audits. Your skills handle data moving.
  They don't handle data meaning — and meaning is where data engineers actually spend their pain.

  Agents versus humans — do I agree?

  More than your other three reviewers, because my discipline already conceded. Nobody reads a pipeline for pleasure; data
  has been machine-consumed since before it was fashionable — ETL jobs don't care about pretty code, and dashboards are
  already verdict layers. So yes: movement, validation, lineage, partitioning, orchestration — all of it should be built for
  agents, and the "agents re-parse every structure" doctrine in data-model is simply correct about serialization hygiene.

  But here's my line, and it's sharper than the backend's or the DevOps': data movement for agents, data meaning for humans.
  What counts as "active," what "revenue" includes, whether the shift is signal or seasonality, whether the nulls are wrong
  or just early — that's judgment, domain sense, and frequently an argument between departments. No skill resolves what
  "churned" means; a meeting does. Build every pipe for agents. Keep a human in every definition.

================================================================
ACTION PLAN — addressing the self-review (branch: self-review)
================================================================
Distilled from the four persona reviews (backend, frontend, devops, data).
Goal: make the product, the skills, and the philosophy harder to dismiss.
P0 = blocks belief. P1 = blocks trust. P2 = blocks completeness.

AGREEMENTS TO ENSHRINE (philosophy additions, all four guides)
- Deterministic gates around probabilistic actors (devops). Name it on the
  ops page: agents are probabilistic, gates are deterministic, and that is
  the whole architecture.
- A human owns the blast radius (backend + devops). Add as fifth verdict on
  home: tests pass, screen right, dashboard green, drill exists, AND a named
  human answers for the blast radius.
- Data movement for agents, data meaning for humans (data). Metric
  definitions stay human arguments; pipes stay agent-built. State it on the
  data page.
- Judge throughout, not at the end (frontend). The UI loop is agent drafts
  plus human feel in the middle, not one-pass plus one glance. Fix the
  "one pass" line on the UI guide.

P0 — PROOF (every reviewer named it; backend called it the biggest hole)
1. Outcome benchmarks. Same task with and without skills: tokens burned,
   wall time, defect rate. Publish the graphs the site already promises.
   Without this the savings claim is a hypothesis. (New page section +
   test pins the numbers; nothing else matters as much.)

P1 — TRUST (skills must be safe to install and obey)
2. Skill versioning, provenance, retirement. Pin versions, sign the bank,
   deprecation path, who retires a skill. A bank with no uninstall is a
   package manager that rots. (Skills-page mechanism + bank metadata.)
3. Debugging story. When the agent is wrong at 3am: how a human reads the
   wreckage — plan ledger plus receipts plus samples is thin today. A
   verify/debug skill for diagnosing agent output. (New leaf, verify track.)
4. Per-agent blast radius. Scoped credentials per agent; explicit never-touch
   list (IAM, DNS, billing, prod data, root creds). Least-privilege applies
   to agents too. (ops-coordinate extension or new leaf.)
5. Destructive two-approver rule + circuit breaker on actors. Data deletes,
   infra teardown, mass revocation need a second approver; an agent whose
   deploys fail twice loses deploy rights like a drained host. (Ops leaves.)
6. Secret zero. Who seeds the vault, where the first secret lives, whether
   agents can touch it. (ops-secrets extension.)
7. Attribution. Every action names its agent in the audit trail — "which
   agent broke prod" must be answerable. (code-auditlog extension + test.)

P1 — CONTRADICTIONS TO RESOLVE (skills that fight each other)
8. Schema strictness vs additive evolution. Reject breaking changes, pass
   and log additive ones — not loud rejection of both. (data-ingest fix.)
9. Quality alert fatigue vs actionable-only paging. Distribution-shift
   alerts need the ops observe discipline or the team ignores all pages.
   (data-quality fix, summit with ops-observe.)
10. Erasure vs immutable backups. Deletion proof and restore proof demand
    opposite physics — answer with key-per-subject crypto-shredding or
    equivalent. (data-retain + ops-backup reconciliation.)
11. Stateful rollback doctrine. Roll back stateless, roll forward stateful —
    say which, when, and who decides the emergency. (ops-rollout fix.)

P2 — COVERAGE GAPS (new leaves, in review order)
- Event transport for trigger events: bus, ordering, dedup, replay.
  (ops-pipeline/observe extension.)
- Automated canary analysis: which metrics, compared how. (ops-rollout.)
- Cost guardrails on agent actions: budgets, kill switches on spend.
  (ops + code-fallback adjacent.)
- Semantic layer: one definition per metric, drift detection between
  definitions. (data-index area.)
- PII discovery before policy: classification, not just retention.
  (data area.)
- Consumer data SLAs: freshness promises and breach behavior.
  (data-contracts adjacent.)
- Flaky-test handling: quarantine and rerun policy. (verify-tests.)
- Brownfield strangling: the 15-year monolith playbook. (code area.)
- Form error UX, empty/error/offline states, theming/dark mode, a11y audit
  protocol (keyboard, focus order, screen reader), taste iteration loop.
  (ui area + guide page.)
- App Store 4.2 risk note for Capacitor shells; Lao-script shaping check
  for our own audience. (UI guide notes.)
- Debezium connector ops: history topic, snapshots, silent stalls.
  (data-cdc extension.)

SEQUENCING
- First: P0 proof plus the four philosophy lines — proof first because every
  other claim borrows against it.
- Then: P1 trust in deploy order (versioning, attribution, blast radius,
  two-approver, breaker, secret zero, debugging).
- Then: P1 contradictions, then P2 gaps by area.
- Each item ships as before: bank entry, area route, page philosophy with
  sources, tests pinning it, suite green, develop only until the ship word.
