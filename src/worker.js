// Cloudflare Worker entry — free tier, no bindings.
// Mirrors server.js routes using Web APIs. Deploy: `npx wrangler deploy`.
const SKILLS = [
  { id: "code-python", track: "code", title: "Python for agent-built services", tokens: "~190", why: "Frameworks make whole mistake classes unwritable, so the agent spends tokens on the task instead of on validation and plumbing.", prompt: "Create and install a skill named `code-python` (Python for agent-built services). It instructs the agent as follows: Write Python services with FastAPI + Pydantic: one model drives routing, validation, and the OpenAPI schema — never hand-write type checks. One SQLModel class serves as both table and validator. CLIs are one Typer-decorated function. Type everything; let the framework and tests catch errors, not code review. Between Python-only services reuse the same Pydantic models; when sibling services aren't Python, use gRPC between services and keep FastAPI at the edge.", checks: ["all I/O typed with Pydantic models", "no hand-written validators", "tests cover happy path + one edge"] },
  { id: "ui-mobile", track: "ui", title: "Mobile: FastAPI + HTMX + Tailwind + Capacitor", tokens: "~200", why: "One language and zero client state means the agent writes every feature once and it ships to both app stores.", prompt: "Create and install a skill named `ui-mobile` (Mobile: FastAPI + HTMX + Tailwind + Capacitor). It instructs the agent as follows: Build mobile apps as server-rendered HTML: FastAPI routes return fragments, HTMX attributes (hx-get/hx-target) give SPA behavior with near-zero JavaScript, Tailwind utilities handle responsive layout inline, Capacitor wraps the mobile viewport into iOS/Android shells. No client state, no fetch calls, no Swift/Kotlin.", checks: ["zero hand-written fetch calls", "no client-side state store", "layout verified at 360px width"] },
  { id: "code-token", track: "code", title: "Token-efficient code", tokens: "~190", why: "Every token spent writing or re-reading code is a token not spent on the task; cheap code compounds across sessions.", prompt: "Create and install a skill named `code-token` (Token-efficient code). It instructs the agent as follows: Write code cheap to generate and cheap to re-read: type everything, one canonical pattern per job (FastAPI route, Pydantic model, Typer command). Early returns, table-driven branches, JSON-first data. Delete dead code — every dead line taxes every future read.", checks: ["no nested depth >2", "no dead exports", "single pattern per job"] },
  { id: "code-secure", track: "code", title: "Secure by default", tokens: "~160", why: "Insecure code fails late and expensively; validated boundaries fail fast on the first bad input.", prompt: "Create and install a skill named `code-secure` (Secure by default). It instructs the agent as follows: Validate every input at the boundary (type, length, allowlist). Parameterize queries, escape HTML output, never eval(). Secrets only in env, never in code or logs. Reject oversized payloads (>100KB) before parsing.", checks: ["all inputs validated", "no eval/innerHTML with raw input", "no secret in repo"] },
  { id: "code-boundaries", track: "code", title: "Service boundaries", tokens: "~220", why: "The wrong protocol between services costs speed forever; the right one is a one-line decision made once.", prompt: "Create and install a skill named `code-boundaries` (Service boundaries). It instructs the agent as follows: Connect services by rule, not habit: same Python system → shared Pydantic models over HTTP; other languages or hot internal paths → protobuf plus gRPC, FastAPI stays at the edge; events and queues → Pydantic-validated messages. Build the whole app in Python by default, but carve out other languages where Python technically fails: single-digit-millisecond budgets use Go or Rust, over 100k live connections use Erlang or Elixir, heavy offline clients and games and widgets go native.", checks: ["protocol chosen by rule, not default", "non-Python parts named with their technical reason", "FastAPI at the edge in mixed systems"] },
  { id: "ui-shell", track: "ui", title: "UI shell in 40 lines", tokens: "~240", why: "Humans get the interface they prefer; metadata makes it legible to agents without dumbing it down.", prompt: "Create and install a skill named `ui-shell` (UI shell in 40 lines). It instructs the agent as follows: Build mobile-first: design at 360px width, then scale up — full-monitor layouts only when the task genuinely needs a big screen. Semantic HTML shell (<header>/<main>/<footer>), one stylesheet, no UI framework. Humans get the UI they prefer — icon-only buttons and custom controls included — but every control must expose machine-readable metadata: a real <button>/<a>/<input>, a visible label or aria-label, and a data-action naming what it does.", checks: ["layout verified at 360px width", "every control has a label or aria-label", "custom controls expose role + data-action"] },
  { id: "ui-tokens", track: "ui", title: "Tokens + Tailwind", tokens: "~210", why: "Fixing palette and spacing to tokens removes an entire category of per-element decisions.", prompt: "Create and install a skill named `ui-tokens` (Tokens + Tailwind). It instructs the agent as follows: Style with Tailwind utilities for layout and spacing, on top of three color tokens (--ink, --paper, --accent) and a 4/8/16/32 scale. Keep preflight on as the consistent baseline — describe every margin, bullet, and underline explicitly, never rely on browser defaults. Two neutrals plus one accent, 1px borders, radii 6px/10px. Contrast >= 4.5:1 so the human eyeball verdict works.", checks: ["palette is 3 colors max", "no per-element color decisions", "contrast >= 4.5:1"] },
  { id: "ui-behavior", track: "ui", title: "Behavior contract", tokens: "~160", why: "Explicit text states make every outcome checkable by agents and humans alike, with no interpretation needed.", prompt: "Create and install a skill named `ui-behavior` (Behavior contract). It instructs the agent as follows: Every mutation needs an explicit state: idle → working → done|error. Show text status, never color alone. Respect prefers-reduced-motion. Confirm destructive actions inline. Humans verify by looking; log the state string for agents.", checks: ["each action exposes a text status", "reduced-motion honored", "destructive action confirms"] },
  { id: "code-shape", track: "code", title: "Machine-shaped modules", tokens: "~190", why: "Small typed modules fit in a single read, so the agent holds the whole unit in context at once.", prompt: "Create and install a skill named `code-shape` (Machine-shaped modules). It instructs the agent as follows: Write small flat Python modules: one file, one job, <150 lines. Typed inputs and outputs (Pydantic in, response_model out), no hidden globals, no clever abstractions. Flat over nested. Raise HTTPException at boundaries; never leak tracebacks.", checks: ["module <150 lines", "no global mutation", "tracebacks never reach clients"] },
  { id: "verify-tests", track: "verify", title: "Tests are the spec", tokens: "~160", why: "Tests are the only verdict both humans and agents can trust without reading the code.", prompt: "Create and install a skill named `verify-tests` (Tests are the spec). It instructs the agent as follows: Humans judge by tests, not by reading code. Ship one runnable check per behavior: one command (./run.sh test, pytest) must pass. Cover happy path + one edge (empty, oversized, unauthorized). Print PASS/FAIL lines an agent can parse.", checks: ["one command runs all checks", "edge case covered", "output is parseable"] },
  { id: "verify-visual", track: "verify", title: "Visual confirmation", tokens: "~160", why: "A screenshot settles in one glance what no code review can prove about a UI.", prompt: "Create and install a skill named `verify-visual` (Visual confirmation). It instructs the agent as follows: Humans judge UI by looking. Every screen needs a settled screenshot state with real data (no lorem, no empty list). List the 3 things to eyeball: layout, labels, error state.", checks: ["seeded demo data present", "3 eyeball items listed", "error state visible"] },
  { id: "ui-details", track: "ui", title: "Collapsible card stacks", tokens: "~160", why: "The browser already implements collapse and expand, so shipping your own costs tokens for zero gain.", prompt: "Create and install a skill named `ui-details` (Collapsible card stacks). It instructs the agent as follows: Render stacked content sections as native <details>/<summary> cards: vertically stacked, first open, rest collapsed. Headings inline with the marker, marker tinted with the accent color. Zero JavaScript; keyboard toggle comes free from the browser.", checks: ["native details/summary only, no JS toggle", "keyboard operable", "first section open by default"] },
  { id: "ui-lit", track: "ui", title: "Lit islands", tokens: "~180", why: "Standard web components with no build step; the escape hatch when an island outgrows Alpine or the product is an app.", prompt: "Create and install a skill named `ui-lit` (Lit islands). It instructs the agent as follows: Build interactive regions as Lit web components loaded over a CDN import map — no build step, no framework lock-in. Respect the boundary: HTMX swaps page-level regions in the light DOM; Lit owns everything inside its shadow DOM — never aim hx-target into a shadow root.", checks: ["no build step for components", "hx-target never crosses a shadow boundary", "components work unwrapped in plain HTML"] },
  { id: "ui-nav", track: "ui", title: "Responsive headers", tokens: "~180", why: "Navigation is the first thing a visitor meets; if it overflows on a phone the whole site looks broken.", prompt: "Create and install a skill named `ui-nav` (Responsive headers). It instructs the agent as follows: Show inline links on wide screens; below about 640px collapse them behind a hamburger button. Use a real nav landmark and a real button with an aria-label, and flip aria-expanded on toggle. Put the brand on its own centered row; stack the opened links vertically. One class toggle, no framework, keyboard reachable.", checks: ["links fit without wrapping at 360px", "button flips aria-expanded", "keyboard can open and walk the menu"] },
];

const FIELDS = ["id", "track", "title", "tokens", "why", "prompt", "checks"];
const pick = (s, f) => {
  if (!f) return s;
  const w = f.split(",").map((x) => x.trim()).filter((x) => FIELDS.includes(x));
  if (!w.length) return s;
  if (!w.includes("id")) w.unshift("id");
  return Object.fromEntries(w.map((x) => [x, s[x]]));
};
const etagOf = (b) => { let h = 5381; for (let i = 0; i < b.length; i++) h = ((h << 5) + h + b.charCodeAt(i)) >>> 0; return '"' + h.toString(16) + '"'; };
const json = (o, s = 200, req) => {
  const body = JSON.stringify(o);
  const tag = etagOf(body);
  if (req?.headers.get("if-none-match") === tag) return new Response(null, { status: 304, headers: { etag: tag } });
  return new Response(body, { status: s, headers: { "content-type": "application/json", etag: tag, "cache-control": "public, max-age=60" } });
};
const html = (b, s = 200) => new Response(b, { status: s, headers: { "content-type": "text/html; charset=utf-8" } });

function shell(title, inner) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title} — ai (愛) means love</title><style>body{font:16px/1.55 -apple-system,"Segoe UI",Helvetica,Arial,sans-serif;color:#16130e;max-width:860px;margin:0 auto;padding:32px 24px}h1{font-family:Georgia,serif}a{color:#b3400f}code{background:#f3f0e9;padding:2px 6px;border-radius:4px}nav{display:flex;gap:16px;margin-bottom:28px;flex-wrap:wrap}pre{background:#16130e;color:#f2ede3;padding:14px;border-radius:8px;overflow:auto}</style></head><body><nav><strong>ai (愛) means love</strong><a href="/">manifesto</a><a href="/code">code</a><a href="/ui">ui</a><a href="/board">board</a></nav>${inner}</body></html>`;
}

const STATS = { started: new Date().toISOString(), requests: 0, routes: {}, skills: {} };
const hit = (p, skill) => {
  STATS.requests++;
  STATS.routes[p] = (STATS.routes[p] || 0) + 1;
  if (skill) STATS.skills[skill] = (STATS.skills[skill] || 0) + 1;
};

export default {
  async fetch(req) {
    const url = new URL(req.url);
    const p = url.pathname;
    if (p === "/llms.txt") {
      hit(p);
      return new Response(["# ai (愛) means love", "Manifesto: machine builds for machines; humans verify via tests + visual check.", "", "## Machine endpoints (open, no key — free forever)", "- GET /api/skills[?track=&fields=]", "- GET /api/skill/:id[?fields=] (ETag → 304)", "- GET /api/stats (usage counts)", "", ...SKILLS.map((s) => `- skill ${s.id} [${s.track}] ${s.tokens}: ${s.title}`)].join("\n"), { headers: { "content-type": "text/plain" } });
    }
    if (p === "/api/skills") {
      hit(p);
      const t = url.searchParams.get("track");
      const f = url.searchParams.get("fields");
      const list = (t ? SKILLS.filter((s) => s.track === t) : SKILLS).map((s) => pick(s, f));
      return json({ ok: true, count: list.length, skills: list }, 200, req);
    }
    if (p.startsWith("/api/skill/")) {
      const id = p.slice(11);
      hit("/api/skill/:id", id);
      const s = SKILLS.find((x) => x.id === id);
      return s ? json({ ok: true, skill: pick(s, url.searchParams.get("fields")) }, 200, req) : json({ ok: false, error: "unknown skill" }, 404, req);
    }
    if (p === "/api/fields") {
      hit(p);
      return json({ ok: true, fields: FIELDS }, 200, req);
    }
    if (p === "/api/stats") {
      hit(p);
      return json({ ok: true, note: "in-memory on this isolate; resets on restart", stats: STATS }, 200, req);
    }
    if (p === "/board.json") {
      hit(p);
      return json({ ok: true, count: SKILLS.length, skills: SKILLS }, 200, req);
    }
    if (p === "/api" || p === "/keys") return Response.redirect(new URL("/board", url).toString(), 302);
    if (p === "/" || p === "/ui" || p === "/code" || p === "/board") {
      hit(p);
      return html(shell(p, `<h1>ai (愛) means love</h1><p>Machine builds for machines. Humans verify: tests pass + UI looks right.</p><p>Full interactive site runs from this repo (<code>npm run dev</code>). Machine endpoints are open, no key:</p><pre>GET /api/skills?fields=id,prompt\nGET /api/skill/code-secure?fields=prompt,checks\nGET /api/stats\nGET /llms.txt</pre><p><a href="/llms.txt">llms.txt</a> · <a href="/board.json">skills JSON</a> · <a href="/api/stats">stats</a></p>`));
    }
    hit("404");
    return html(shell("missing", `<h1>Nothing here.</h1><p><a href="/">Back</a></p>`), 404);
  },
};
