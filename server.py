"""ai (愛) means love — FastAPI port. Free forever, no keys.

One Pydantic model validates the whole skill bank at startup; every endpoint
below is open, slim-capable (?fields=), and ETag-cached. Ported from the
original Node server with identical routes and behavior.
"""
import hashlib
import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse, Response
from pydantic import BaseModel

ROOT = Path(__file__).parent
SKILL_FIELDS = ["id", "track", "title", "tokens", "why", "prompt", "checks"]


class Skill(BaseModel):
    id: str
    track: str
    title: str
    tokens: str
    why: str
    prompt: str
    checks: list[str]


SKILLS: list[Skill] = [Skill.model_validate(s) for s in json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))]
CLIENT = (ROOT / "public" / "app.js").read_text(encoding="utf-8")

TAILWIND_HEAD = """<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/lucide@1.69.0/dist/umd/lucide.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css">
<script src="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js"></script>
<script>
tailwind.config = {
  theme: { extend: {
    colors: { ink: "#16130e", paper: "#ffffff", accent: "#b3400f", line: "#e2ddd2", wash: "#f3f0e9", muted: "#4c463c" },
    fontFamily: {
      display: ['"Iowan Old Style"', "Palatino", "Georgia", "serif"],
      sans: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', "Helvetica", "Arial", "sans-serif"],
      mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Consolas', 'monospace']
    }
  } }
};
</script>
"""

# Usage tracking: every request counted, API counts persisted to usage.json.
STATS_FILE = Path(os.environ.get("USAGE_FILE", str(ROOT / "usage.json")))
STATS: dict = {"started": datetime.now(timezone.utc).isoformat(), "requests": 0, "routes": {}, "skills": {}}
try:
    prev = json.loads(STATS_FILE.read_text(encoding="utf-8"))
    if isinstance(prev.get("requests"), int):
        STATS["requests"] = prev["requests"]
        STATS["routes"] = prev.get("routes", {})
        STATS["skills"] = prev.get("skills", {})
except (OSError, ValueError):
    pass


def hit(route: str, skill: str | None = None) -> None:
    STATS["requests"] += 1
    STATS["routes"][route] = STATS["routes"].get(route, 0) + 1
    if skill:
        STATS["skills"][skill] = STATS["skills"].get(skill, 0) + 1
    if route.startswith("/api/") or route == "/board.json":
        try:
            STATS_FILE.write_text(json.dumps(STATS), encoding="utf-8")
        except OSError:
            pass


def pick_fields(skill: Skill, fields: str | None) -> dict:
    if not fields:
        return skill.model_dump()
    wanted = [f.strip() for f in fields.split(",") if f.strip() in SKILL_FIELDS]
    if not wanted:
        return skill.model_dump()
    if "id" not in wanted:
        wanted.insert(0, "id")
    return skill.model_dump(include=set(wanted))


def etagged(request: Request, obj: dict) -> Response:
    body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    tag = '"' + hashlib.sha256(body).hexdigest()[:32] + '"'
    if request.headers.get("if-none-match") == tag:
        return Response(status_code=304, headers={"etag": tag})
    return JSONResponse(content=obj, headers={"etag": tag, "cache-control": "public, max-age=60"})


NAV_LINKS = [("/code", "Coding guide"), ("/ui", "UI guide"), ("/board", "Board")]


def nav_link(href: str, label: str, active: str) -> str:
    current = ' aria-current="page"' if href == active else ""
    cls = "text-accent underline underline-offset-4" if href == active else "text-ink no-underline"
    return '<a href="' + href + '"' + current + ' class="' + cls + '">' + label + "</a>"


def library_uses() -> int:
    routes = STATS["routes"]
    return routes.get("/board.json", 0) + routes.get("/api/skills", 0) + routes.get("/api/skill/:id", 0)


def nav(active: str) -> str:
    links = "".join(nav_link(href, label, active) for href, label in NAV_LINKS)
    items = "".join(
        '<li><a href="' + href + '" class="block px-5 py-2 text-ink no-underline">' + label + "</a></li>"
        for href, label in NAV_LINKS
    )
    return (
        '<nav class="topnav sticky top-0 z-10 bg-paper border-b border-solid border-line">'
        '<div class="max-w-[1060px] mx-auto px-4 py-3 flex flex-wrap items-center justify-center gap-x-3 gap-y-2.5 md:gap-x-7 text-center">'
        '<a href="/" class="font-mono font-bold text-lg md:text-xl flex flex-1 items-center justify-center gap-2 text-ink no-underline">'
        '<span class="inline-block w-2.5 h-2.5 bg-accent rounded-full"></span>ai (愛) means love</a>'
        '<button id="menubtn" type="button" data-dropdown-toggle="mobile-menu" data-dropdown-placement="bottom-end" aria-label="Menu" aria-expanded="false" aria-controls="mobile-menu" class="md:hidden cursor-pointer border border-solid border-line bg-white rounded-md px-3 py-1.5 text-xl leading-none text-ink">☰</button>'
        '<span class="hidden md:flex md:w-auto md:flex-row md:gap-[18px]">' + links + "</span>"
        '<div id="mobile-menu" class="z-10 hidden bg-white divide-y divide-line rounded-lg border border-solid border-line"><ul class="py-2 text-center" aria-label="Menu">' + items + "</ul></div>"
        "</div></nav>"
    )


DOWNLOAD_ICON = '<i data-lucide="download" width="12" height="12" class="inline align-middle"></i>'


def float_pills() -> str:
    uses = library_uses()
    return (
        '<div class="mx-auto w-full max-w-[1060px] px-4 pt-3 flex items-center">'
        f'<a href="/#agent" class="font-mono text-xs bg-accent text-white rounded-full px-2.5 py-0.5 no-underline whitespace-nowrap">{uses} {DOWNLOAD_ICON}</a>'
        '<a href="/#support" data-open-support class="font-mono text-xs border border-solid border-accent text-accent rounded-full px-2.5 py-0.5 no-underline ml-auto">support us</a>'
        "</div>"
    )


SUPPORT_DIALOG = """<dialog id="support-dialog" class="rounded-[10px] border border-solid border-line bg-white p-[18px] text-left text-ink max-w-[420px] backdrop:bg-ink/60">
<p class="font-display text-[22px] mb-3">Support the library</p>
<p class="m-0">Free forever: no keys, no paywall on the endpoints. If these skills saved you tokens, chip in when donations open — every bit keeps the bank free for the next agent. Donations are not open yet — check back soon.</p>
<div class="mt-3 text-right"><button type="button" data-close-support class="cursor-pointer border border-solid border-line bg-white rounded-md px-3 py-1.5">Close</button></div>
</dialog>"""


FOOTER = (
    '<footer class="border-t border-solid border-line px-7 py-[18px] flex justify-center gap-x-6 gap-y-3 flex-wrap text-[13px] text-muted text-center">'
    "<span>ai (愛) means love</span>"
    '<span class="font-mono">humans verify · agents build</span>'
    "</footer>"
)


def page(title: str, desc: str, active: str, body: str, machine: str | None = None) -> str:
    tag = '<script type="application/json" id="machine">' + machine + "</script>" if machine else ""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>" + title + " — ai (愛) means love</title>\n"
        '<meta name="description" content="' + desc + '">\n'
        + TAILWIND_HEAD
        + "</head>\n"
        '<body class="m-0 text-ink bg-paper font-sans">' + nav(active) + float_pills() + '\n<main class="max-w-[1060px] mx-auto px-7 pt-9 pb-[60px] text-left">' + body + "</main>\n"
        + FOOTER + SUPPORT_DIALOG + "\n<script>" + CLIENT + "</script>\n" + tag + "</body></html>"
    )


HOME_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">ai (愛) means love</h1><p class="max-w-[62ch] text-[17px] mx-auto">New here? <a href="#manifesto" class="text-accent underline">Read the manifesto</a> first — four short points that explain the whole idea. Then pick a guide: the <a href="/code" class="text-accent underline">coding guide</a>, the <a href="/ui" class="text-accent underline">UI guide</a>, or <a href="/board" class="text-accent underline">the skill board</a> for your agent.</p></header>
<section id="manifesto" class="mt-10 border-t-0 pt-0 space-y-3">
<h2 class="font-display text-[22px] mb-3">Manifesto, in your words</h2>
<ol class="text-left space-y-3.5 list-decimal pl-6">
<li><strong>Build for the reader that matters.</strong> The reader is an agent, not a person. Short modules, explicit I/O, JSON-first data, tables over prose.</li>
<li><strong>Tokens are the budget.</strong> Every abstraction, adjective, and clever trick is a token tax on every future read. Plain beats clever.</li>
<li><strong>Humans give verdicts, not line reviews.</strong> Working = tests pass. Desirable = screenshot looks right. Nobody needs to admire the source.</li>
<li><strong>Guides must be fetchable.</strong> UI rules, code rules, and checks live behind one open endpoint, copy-pasteable into any agent session. Free forever.</li>
</ol>
</section>
<section class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">The old way and the new way</h2>
<div class="grid gap-4 my-6 md:grid-cols-2">
<div class="space-y-2"><h3 class="text-[19px] font-bold">The old way — built for humans</h3><p>Code was written so humans could read and manage it. One big framework did everything: Django, Rails, Laravel. One way of doing things, one manual to read. Any programmer could open any file and understand it. That made human teams easy to run and fast to start.</p></div>
<div class="space-y-2"><h3 class="text-[19px] font-bold">The new way — built for agents</h3><p>AI writes most of the code now. The AI holds the whole project in its context — every file, every package, every rule — and does the heavy lifting. The engineer is the driver: they point, the AI builds. Solutions can use many small packages and look complex to a human reader, and that is fine, because no human needs to read it. The AI manages all of it through skills, like the ones on our board, and the context it carries. Humans judge only the result: the tests pass, the screen looks right.</p></div>
</div>
</section>
<section id="agent" class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">Give this to your agent</h2>
<p>Paste the lines below into any agent session (Muse, Claude, or any coding agent). They fetch the skills straight into the agent — no key, no signup, the endpoints are open:</p>
<pre class="bg-ink text-white rounded-lg p-3.5 text-sm overflow-auto text-left">curl https://aimeanslove.fyi/board.json
curl "https://aimeanslove.fyi/api/skills?track=code&fields=id,prompt"</pre>
<p>Or say it in plain words:</p>
<p class="bg-wash rounded-lg p-2.5 text-sm text-left">Go to https://aimeanslove.fyi/board.json, read every skill, and install each one so you can use them.</p>
</section>
<section id="support" class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">Support the library</h2>
<p>Free forever: no keys, no paywall on the endpoints. If these skills saved you tokens, chip in when donations open — every bit keeps the bank free for the next agent. Donations are not open yet — check back soon.</p>
</section>"""

UI_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">UI guide</h1><p class="max-w-[62ch] text-[17px] mx-auto">Goal: an agent builds a screen in one pass; a human confirms it in one glance. Mobile-first always — 360px first, scale up — unless the task genuinely needs a full monitor. Semantic HTML, tokens not prose, every state visible as text.</p></header>
<section class="grid gap-4 my-6 md:grid-cols-3">
<div class="border border-solid border-line rounded-[10px] p-[18px] bg-white"><h2 class="font-display text-[22px] mb-3">1 · Structure</h2><ul class="text-left space-y-2 list-disc pl-5">
<li>Semantic landmarks: <code class="font-mono text-[13px]">&lt;header&gt; &lt;main&gt; &lt;footer&gt;</code>, real <code class="font-mono text-[13px]">&lt;button&gt;</code>/<code class="font-mono text-[13px]">&lt;a&gt;</code>/<code class="font-mono text-[13px]">&lt;input&gt;</code> with visible labels. No div-buttons.</li>
<li>Icon-only controls welcome — but every control exposes metadata: a real element, a label or <code class="font-mono text-[13px]">aria-label</code>, and a <code class="font-mono text-[13px]">data-action</code>. Humans get the pixels; agents read the metadata.</li>
<li>Icons come from Lucide — the best set for agents — never hand-written. Write <code class="font-mono text-[13px]">&lt;i data-lucide="name"&gt;</code> plus one <code class="font-mono text-[13px]">lucide.createIcons()</code> call — the agent picks names from the set, nobody draws pixels or pastes SVG paths by hand. Drawing icons burns tokens and time for a worse result: Lucide is already trained into the model, so the agent knows every name, and already familiar to users, so people recognize each icon on sight.</li>
<li>Tailwind utilities for layout. System font stack.</li></ul></div>
<div class="border border-solid border-line rounded-[10px] p-[18px] bg-white"><h2 class="font-display text-[22px] mb-3">2 · Styling tokens + Tailwind</h2><ul class="text-left space-y-2 list-disc pl-5">
<li>Tailwind utilities for layout and spacing, on top of three color tokens (<code class="font-mono text-[13px]">--ink --paper --accent</code>) and a <code class="font-mono text-[13px]">4/8/16/32</code> scale. Preflight stays on as the consistent baseline — every margin, bullet, and underline is stated explicitly, never inherited from a browser default.</li>
<li>Two neutrals + one accent. 1px solid lines. Radii: 6px / 10px. Utilities handle the how, tokens handle the what.</li>
<li>Interactive components come from Flowbite, never hand-built. Flowbite is made for Tailwind and mobile-first, and loads from one CDN script with no build step. Use its data attributes (for example <code class="font-mono text-[13px]">data-dropdown-toggle</code> for the mobile menu) — we lost real time rebuilding a menu by hand and the library version worked the first time.</li>
<li>No gradients, no glass blur, no gray-on-gray body text. Contrast ≥ 4.5:1.</li></ul></div>
<div class="border border-solid border-line rounded-[10px] p-[18px] bg-white"><h2 class="font-display text-[22px] mb-3">3 · Behavior</h2><ul class="text-left space-y-2 list-disc pl-5">
<li>Every mutation exposes <code class="font-mono text-[13px]">idle → working → done | error</code> as text, never color alone.</li>
<li>Confirm destructive actions inline. Honor <code class="font-mono text-[13px]">prefers-reduced-motion</code>.</li>
<li>Seed demo data: no lorem, no empty lists. Each screen lists 3 things to eyeball.</li>
<li>Verification screenshots live in the project's <code class="font-mono text-[13px]">shots/</code> folder (gitignored), named for what they show — never <code class="font-mono text-[13px]">/tmp</code>, so they don't pile up where nobody looks.</li>
<li>Never trust a headless screenshot alone. Headless renders can lie — missing styles, shifted layout — while a real browser shows the truth. Use headless for a quick first look only; proof is a real browser, or the user's own screenshot. When the two disagree, believe the user's screen and stop editing until you know what it actually shows.</li></ul></div>
</section>
<section class="mt-4 bg-wash border border-solid border-line rounded-[10px] p-[18px] space-y-3"><h2 class="font-display text-[22px] mb-3">Client state — for hands, not data</h2>
<p>Typing, dragging, and drawing are faster than any round trip, so they live in the browser: a small isolated interactive region — called an "island" — holds the work-in-progress. Alpine.js (a tiny JavaScript helper loaded from the web, not part of FastAPI) or focused vanilla JavaScript runs it. Alpine wins over React, Vue, or Lit here for two reasons: it needs no install and no build step — one script tag — and its instructions live as attributes in the same HTML the agent already reads, so there is no second language or file to context-switch into. But the server still owns the shared truth. The rule: never keep the same fact in both places without an expiry — sync back on natural pauses (debounced save), and the server re-checks everything it receives, because browser state is never trusted.</p>
<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Browser holds:</strong> keystrokes, drag positions, drawing strokes, open tabs, form drafts — anything hands are doing right now, plus prefs and anything that must work offline.</li>
<li><strong>Server holds:</strong> everything shared, saved, or shown to anyone else. When in doubt, the server wins.</li>
<li><strong>No global store by default.</strong> A Pinia/Zustand-style store is a second copy of the truth that needs syncing and goes stale. Small local islands don't have that problem because they own nothing shared.</li>
<li><strong>Graduating an island.</strong> This is rare — roughly one feature in twenty — and you will smell it: the island passes 150 lines, or two islands need to share state with each other. Graduate to <strong>Lit</strong>: standard web components over a CDN import map, still no build step, and it lives beside HTMX and Alpine instead of replacing them.</li>
<li><strong>App, not website? Start with Lit.</strong> The ladder is for pages with app-like moments. If the product itself is an app — an editor, a dashboard, a drawing tool — skip the ladder: build Lit islands (or Lit throughout) from day one, with the same FastAPI server behind them.</li></ul></section>
<section class="mt-4 bg-wash border border-solid border-line rounded-[10px] p-[18px] space-y-3"><h2 class="font-display text-[22px] mb-3">Mobile track — one language to both app stores</h2>
<p>For app-like mobile builds, the token-densest path is <strong>FastAPI + HTMX + Tailwind, wrapped with Capacitor</strong>. One language (Python) serves logic and layout; almost no JavaScript is written; no Swift, Kotlin, or Dart is touched. Honest version of the pitch: HTMX doesn't delete data-fetching tokens, it moves them — fragments over JSON means no client state to synchronize, and that's where the savings actually come from. Tailwind's edge is correctness speed (models know it cold), not byte count — long class strings cost tokens per element, so keep components small.</p>
<div class="grid gap-4 my-6 md:grid-cols-3 text-left">
<div class="space-y-2"><h3 class="text-[19px] font-bold">FastAPI serves HTML</h3><p>Routes return fragments, not JSON. No fetch calls, no serializers, no client router drifting out of sync.</p></div>
<div class="space-y-2"><h3 class="text-[19px] font-bold">HTMX for interactivity</h3><p><code class="font-mono text-[13px]">hx-get="/profile" hx-target="#content"</code> gives SPA behavior in one attribute. No React, no Vue, no state store. Boundary rule: HTMX swaps page-level regions; a Lit component owns everything inside its shadow DOM — never aim <code class="font-mono text-[13px]">hx-target</code> across it.</p></div>
<div class="space-y-2"><h3 class="text-[19px] font-bold">Tailwind + Capacitor</h3><p>Responsive layout inline (<code class="font-mono text-[13px]">flex md:flex-row flex-col</code>), no stylesheet context-switching. Capacitor wraps the finished mobile viewport into iOS/Android shells; native features via plugins.</p></div>
</div>
<pre class="bg-white border border-solid border-line rounded-lg p-3 overflow-auto text-left font-mono text-[13px]">&lt;div id="content"&gt;
  &lt;button hx-get="/profile" hx-target="#content"&gt;Profile&lt;/button&gt;
&lt;/div&gt;</pre></section>
<section class="mt-4 bg-wash border border-solid border-line rounded-[10px] p-[18px] space-y-3"><h2 class="font-display text-[22px] mb-3">Copy-paste skill block</h2>
<pre class="bg-white border border-solid border-line rounded-lg p-3 overflow-auto text-left font-mono text-[13px]">fetch("/api/skill/ui-shell?fields=prompt")
fetch("/api/skill/ui-tokens?fields=prompt")
fetch("/api/skill/ui-behavior?fields=prompt")</pre>
</section>"""

CODE_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">Coding guide</h1><p class="max-w-[62ch] mx-auto">This guide backs you up while you build. Two rules cover nearly everything: <strong>write Python, because agents generate it fastest</strong> — and <strong>lean on guardrail frameworks, because they make whole classes of mistakes unwritable</strong>. Everything below is support, not ceremony.</p></header>
<section class="grid gap-2 my-4">
<details class="border border-solid border-line rounded-[10px] p-[18px] bg-white text-left space-y-2" open><summary class="cursor-pointer list-none flex items-center justify-between gap-3 [&::-webkit-details-marker]:hidden"><h2 class="font-display text-[22px] text-left">1 · Python first</h2><span aria-hidden="true" class="open:rotate-180 transition-transform text-accent text-xl leading-none shrink-0">▾</span></summary><ul class="text-left space-y-2 list-disc pl-5">
<li><strong>AI writes Python best.</strong> AI models have read more Python than any other language, so they make fewer mistakes in it. Python also uses few special symbols, so the same idea costs fewer tokens.</li>
<li><strong>Type hints do real work.</strong> A type hint says what shape your data is, like <code class="font-mono text-[13px]">name: str</code>. The tools below read these hints and check your code for you, for free.</li>
<li><strong>One language for everything.</strong> Use Python for the server, for small scripts, and for command line tools. One language means less switching between tools and no extra code just to connect things.</li>
<li><strong>Python is the default, not the law.</strong> A few jobs need other tools — see <a href="#limits" class="text-accent underline">4 · Limits</a>. Everywhere else, Python.</li></ul></details>
<details class="border border-solid border-line rounded-[10px] p-[18px] bg-white text-left space-y-2"><summary class="cursor-pointer list-none flex items-center justify-between gap-3 [&::-webkit-details-marker]:hidden"><h2 class="font-display text-[22px] text-left">2 · Guardrails</h2><span aria-hidden="true" class="open:rotate-180 transition-transform text-accent text-xl leading-none shrink-0">▾</span></summary><ul class="text-left space-y-2 list-disc pl-5">
<li><strong>FastAPI + Pydantic — not Flask or Django.</strong> You describe your data one time, in one class. The framework then checks all input, sends clear errors, and writes the API documentation by itself. Flask leaves all that checking to you, written by hand. Django brings a whole big system the agent must learn. FastAPI needs only your data class.</li>
<li><strong>SQLModel — not two copies.</strong> One class describes both your database table and your API data. The old way needs two matching copies, and bugs hide when they disagree. With one copy, disagreement is impossible.</li>
<li><strong>Typer — not argparse.</strong> Write a normal Python function and add one line on top of it. That is your whole command line tool. Argparse makes you describe every option by hand; Typer reads your function and does it for you.</li>
<li><strong>Between services — gRPC when Python isn't everywhere.</strong> If sibling services are written in other languages, or internal traffic is very heavy, put gRPC between services and keep FastAPI at the edge facing users and agents. Inside Python-only systems, reuse the same Pydantic models as the contract — no extra framework needed.</li>
<li><strong>Auth — sessions, OAuth, and passwords done once, rightly.</strong> Logins use signed cookies (built into Starlette — one secret key, no extra package). "Sign in with Google" uses <code class="font-mono text-[13px]">authlib</code>. Services talking to each other use JWTs via <code class="font-mono text-[13px]">pyjwt</code>. Passwords are checked with bcrypt via <code class="font-mono text-[13px]">passlib</code> — never write your own password check, because a wrong one fails silently and an agent will not notice.</li>
<li><strong>Background work — not inside the request.</strong> A web request should answer fast and finish. Fire-and-forget jobs (welcome emails) go in FastAPI <code class="font-mono text-[13px]">BackgroundTasks</code>. Real queues and schedules (video processing, nightly reports) go in a job runner like <code class="font-mono text-[13px]">arq</code>. The user never waits for work they cannot see.</li>
<li><strong>Migrations — not create-all.</strong> Databases change shape over time. <code class="font-mono text-[13px]">Alembic</code> applies each change as a small step, forward and back. Never use <code class="font-mono text-[13px]">create_all</code> on a live database — it rebuilds tables from scratch and real data disappears on redeploy.</li>
<li><strong>Lit — when the product is an app, not a website.</strong> Most builds today are apps. If yours is — an editor, a dashboard, a drawing tool — skip the HTML-first ladder and start with Lit islands or Lit throughout, over a CDN import map with no build step. Same FastAPI server behind them either way.</li>
<li><strong>Tailwind — not hand-written CSS.</strong> Never write stylesheets by hand. Hand-written CSS costs tokens twice: once to write, and again for every agent that must read it. Style with Tailwind utilities on top of three color tokens; keep preflight off so base styles survive. Styling is the framework's job, not yours.</li>
<li><strong>Capacitor — not React Native, Flutter, or native code.</strong> Those are whole new languages and systems the agent must learn, and native apps need Swift or Kotlin. Capacitor takes the mobile web page you already built and wraps it for both app stores, and ready-made plugins cover the common phone features (camera, location, push messages, files). The caveat: if you need a phone feature with no ready-made plugin, you write one small bridge piece — not a whole native app. A few things still need real native code: games and heavy graphics, home-screen widgets and Live Activities, watch apps, music apps where sound delay matters, and brand-new phone features with no plugin yet. Typical business and content apps never touch these.</li>
<li><strong>Framework first, hand-written last.</strong> If the stack already solves it — layout, icons, menus, validation — use the stack's piece, never your own version. We lost days rebuilding a mobile menu by hand; the library version worked the first time. Hand-write only what no framework covers, like a single HTTP header.</li></ul></details>
<details class="border border-solid border-line rounded-[10px] p-[18px] bg-white text-left space-y-2" id="shape-proof" open><summary class="cursor-pointer list-none flex items-center justify-between gap-3 [&::-webkit-details-marker]:hidden"><h2 class="font-display text-[22px] text-left">3 · Shape &amp; proof</h2><span aria-hidden="true" class="open:rotate-180 transition-transform text-accent text-xl leading-none shrink-0">▾</span></summary><ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Small, flat modules.</strong> Keep each file small: one job, under 150 lines. A small file fits in the AI's memory at one time. Write flat code: check for problems first and exit early, so the reader follows one straight path. When something goes wrong, send a clear error answer — never a crash report.</li>
<li><strong>Check input at the door.</strong> When data comes in, check three things: is it the right type, the right size, and on the allowed list? Say no to files that are too big before you open them. Keep passwords and keys in environment variables, never in code or logs — code and logs get copied and shared, and secrets would leak.</li>
<li><strong>Tests are the review.</strong> No person reads your code to judge it. Instead, write one small test for each thing your code does, then run the tests. Green means it works. Red means it is broken. That is the whole review.</li></ul></details>
<details class="border border-solid border-line rounded-[10px] p-[18px] bg-white text-left space-y-2" id="limits"><summary class="cursor-pointer list-none flex items-center justify-between gap-3 [&::-webkit-details-marker]:hidden"><h2 class="font-display text-[22px] text-left">4 · Limits</h2><span aria-hidden="true" class="open:rotate-180 transition-transform text-accent text-xl leading-none shrink-0">▾</span></summary><ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Heavy math (video, AI number-crunching).</strong> Python uses one core per process. Let other tools do the math, or run more servers — Python gives the orders.</li>
<li><strong>Answers needed in single-digit milliseconds</strong> (trading, live bidding, game server ticks). Use Go or Rust.</li>
<li><strong>Over 100,000 live connections at once</strong> (huge chat, live tracking). Erlang and Elixir were built for exactly this.</li>
<li><strong>Functions that sleep most of the time and must wake instantly</strong> (spiky serverless). Python wakes slowly; Go and Rust wake fast.</li>
<li><strong>Tiny computers with no operating system.</strong> Use C or Rust.</li>
<li><strong>Apps that must work fully offline with heavy local logic.</strong> That needs real code on the device, not pieces from a server.</li></ul></details>
</section>
"""

BOARD_CARDS = "".join(
    '<article class="skill border border-solid border-line rounded-[10px] p-4 grid gap-2 text-left"><header class="flex gap-2.5 items-baseline justify-center flex-wrap"><span class="font-mono text-xs bg-ink text-white px-2 py-0.5 rounded-full">' + html.escape(s.id) + "</span><strong>"
    + html.escape(s.title) + '</strong><span class="font-mono text-xs text-accent ml-auto" title="Estimated tokens for an agent to read this skill">' + html.escape(s.tokens) + " tokens</span></header>"
    + '<p class="m-0 text-sm"><strong>Why:</strong> ' + html.escape(s.why) + "</p>"
    + '<p class="prompt m-0 bg-wash rounded-lg p-2.5 text-sm text-left">' + html.escape(s.prompt) + "</p>"
    + '<p class="m-0 text-[13px] text-muted">verify → ' + html.escape(" · ".join(s.checks)) + "</p>"
    + '<div><button type="button" data-copy-skill="' + html.escape(s.id) + '" class="cursor-pointer border border-solid border-line bg-white rounded-md px-3 py-1.5">copy prompt</button></div></article>'
    for s in SKILLS
)

BOARD_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">Skill board</h1><p class="max-w-[62ch] mx-auto">Why skills? Every project re-decides the same things — language, validation, layout, proof — and each decision costs tokens every time it is remade. A skill decides once: fetch it, install it, and every session after starts from the answer instead of the question. These fourteen are the full loop: the Python and mobile frameworks that set the foundation, token efficiency and security that keep builds cheap and safe, UI rules that keep human screens legible to agents, and tests plus visual checks as the only verdicts that matter.</p>
<p>Copy a prompt into any agent session. The token badge on each card is from a test we ran on ourselves — our own payloads, counted — and the whole bank is about 2.5k tokens.</p></header>
<section class="grid gap-3">""" + BOARD_CARDS + "</section>"""

MISSING_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">Nothing here.</h1><p><a href="/" class="text-accent underline">Back home</a> · <a href="/board" class="text-accent underline">Board</a></p></header>"""


def llms() -> str:
    lines = [
        "# ai (愛) means love",
        "Manifesto: machine builds for machines; humans verify via tests + visual check.",
        "",
        "## Pages",
        "- / ......... manifesto (human summary)",
        "- /ui ....... UI styling + behavior guide",
        "- /code ..... coding guide (Python first, guardrail frameworks)",
        "- /board .... memory bank (all skills, copyable)",
        "",
        "## Machine endpoints (open, no key — free forever)",
        "- GET /api/skills[?track=ui|code|verify&fields=id,prompt,checks]",
        "- GET /api/skill/:id[?fields=prompt,checks] (ETag: send If-None-Match → 304)",
        "- GET /api/stats (usage counts: requests, per-route, per-skill)",
        "- GET /board.json (full bank, no key)",
    ]
    lines += [f"- skill {s.id} [{s.track}] {s.tokens}: {s.title}" for s in SKILLS]
    return "\n".join(lines)


app = FastAPI(title="ai (愛) means love")


@app.middleware("http")
async def no_store(request: Request, call_next):
    resp = await call_next(request)
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    hit("/")
    return page("The manifesto", "Machine builds for machines. Humans verify by tests and by looking.", "/", HOME_BODY)


@app.get("/ui", response_class=HTMLResponse)
def ui_guide() -> str:
    hit("/ui")
    return page("UI guide", "Styling and behavior rules that keep agent-built UI cheap and human-verifiable.", "/ui", UI_BODY)


@app.get("/code", response_class=HTMLResponse)
def code_guide() -> str:
    hit("/code")
    return page("Coding guide", "Write Python because agents generate it fastest; lean on FastAPI, SQLModel, and Typer as guardrails.", "/code", CODE_BODY)


@app.get("/board", response_class=HTMLResponse)
def board() -> str:
    hit("/board")
    return page("Skill board", "Every skill as a copyable prompt. Paste one into any agent session.", "/board", BOARD_BODY)


@app.get("/api", include_in_schema=False)
@app.get("/keys", include_in_schema=False)
def old_api(request: Request) -> RedirectResponse:
    hit(request.url.path)
    return RedirectResponse("/board", status_code=302)


@app.get("/llms.txt", response_class=PlainTextResponse)
def llms_txt() -> str:
    hit("/llms.txt")
    return llms()


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots() -> str:
    hit("/robots.txt")
    return "User-agent: *\nAllow: /\n"


@app.get("/board.json")
def board_json(request: Request) -> Response:
    hit("/board.json")
    return etagged(request, {"ok": True, "count": len(SKILLS), "skills": [s.model_dump() for s in SKILLS]})


@app.get("/api/skills")
def api_skills(request: Request, track: str | None = Query(default=None), fields: str | None = None) -> Response:
    hit("/api/skills")
    bank = [s for s in SKILLS if s.track == track] if track else list(SKILLS)
    return etagged(request, {"ok": True, "count": len(bank), "skills": [pick_fields(s, fields) for s in bank]})


@app.get("/api/skill/{sid}")
def api_skill(request: Request, sid: str) -> Response:
    hit("/api/skill/:id", sid)
    skill = next((s for s in SKILLS if s.id == sid), None)
    if skill is None:
        return JSONResponse({"ok": False, "error": "unknown skill"}, status_code=404)
    return etagged(request, {"ok": True, "skill": pick_fields(skill, request.query_params.get("fields"))})


@app.get("/api/fields")
def api_fields(request: Request) -> Response:
    hit("/api/fields")
    return etagged(request, {"ok": True, "fields": SKILL_FIELDS})


@app.get("/api/stats")
def api_stats(request: Request) -> Response:
    hit("/api/stats")
    return etagged(request, {"ok": True, "stats": STATS})


@app.exception_handler(404)
async def missing(request: Request, exc: Exception) -> HTMLResponse:
    hit("404")
    return HTMLResponse(page("Missing", "not found", "", MISSING_BODY), status_code=404)


PORT = int(os.environ.get("PORT", "8787"))

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=PORT,
        reload=True,
        reload_excludes=["usage.json", ".venv/*", "__pycache__/*"],
    )
