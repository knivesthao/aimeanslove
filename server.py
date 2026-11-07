"""ai (愛) means love — FastAPI port. Skill JSON behind a $9.99 forever key; guides and stats stay open.

One Pydantic model validates the whole skill bank at startup; every endpoint
below is open, slim-capable (?fields=), and ETag-cached. Ported from the
original Node server with identical routes and behavior.
"""
import hashlib
import html
import json
import os
import time
import urllib.request
from collections import deque
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
<style type="text/tailwindcss">
@layer base {
  :focus-visible { @apply outline-2 outline-accent outline-offset-2; }
  main p, main li { max-width: 72ch; }
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
}
</style>
"""

# Usage tracking: every request counted, API counts persisted to usage.json.
# Copy-prompt clicks land in a pending bucket; the public counter absorbs them
# at most once per rollup window (daily in prod), so the badge moves slowly.
ROLLUP_SECONDS = int(os.environ.get("COPY_ROLLUP_SECONDS", "86400"))
STATS_FILE = Path(os.environ.get("USAGE_FILE", str(ROOT / "usage.json")))
STATS: dict = {
    "started": datetime.now(timezone.utc).isoformat(),
    "requests": 0,
    "routes": {},
    "skills": {},
    "copies_applied": 0,
    "pending_copies": 0,
    "install_receipts": 0,
    "install_versions": {},
    "last_rollup": datetime.now(timezone.utc).isoformat(),
}
try:
    prev = json.loads(STATS_FILE.read_text(encoding="utf-8"))
    if isinstance(prev.get("requests"), int):
        STATS["requests"] = prev["requests"]
        STATS["routes"] = prev.get("routes", {})
        STATS["skills"] = prev.get("skills", {})
        STATS["copies_applied"] = prev.get("copies_applied", 0)
        STATS["pending_copies"] = prev.get("pending_copies", 0)
        STATS["install_receipts"] = prev.get("install_receipts", 0)
        STATS["install_versions"] = prev.get("install_versions", {})
        STATS["last_rollup"] = prev.get("last_rollup", STATS["last_rollup"])
except (OSError, ValueError):
    pass


def rollup_copies() -> None:
    try:
        last = datetime.fromisoformat(STATS["last_rollup"])
    except (ValueError, TypeError):
        last = datetime.now(timezone.utc)
    if (datetime.now(timezone.utc) - last).total_seconds() >= ROLLUP_SECONDS and STATS["pending_copies"] > 0:
        STATS["copies_applied"] += STATS["pending_copies"]
        STATS["pending_copies"] = 0
        STATS["last_rollup"] = datetime.now(timezone.utc).isoformat()
        try:
            STATS_FILE.write_text(json.dumps(STATS), encoding="utf-8")
        except OSError:
            pass


KEYS_FILE = Path(os.environ.get("AILV_KEYS_FILE", str(ROOT / "keys.json")))


def _load_keys() -> dict:
    try:
        db = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
        return db.get("keys", {}) if isinstance(db, dict) else {}
    except (OSError, ValueError):
        return {}


def _check_key(raw: str) -> str | None:
    digest = hashlib.sha256(raw.encode()).hexdigest()
    entry = _load_keys().get(digest)
    return digest if entry and entry.get("active", True) else None


def _touch_key(digest: str) -> None:
    try:
        db = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
        db["keys"][digest]["uses"] = db["keys"][digest].get("uses", 0) + 1
        KEYS_FILE.write_text(json.dumps(db, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError):
        pass


def _require_key(request: Request) -> str | JSONResponse:
    """Gate a skill-JSON endpoint on a valid forever key. Returns the key digest or a 403."""
    raw = (request.query_params.get("key") or "").strip()
    if not raw:
        return JSONResponse({"ok": False, "error": "key required — one $9.99 key unlocks the bank forever"}, status_code=403)
    digest = _check_key(raw)
    if not digest:
        return JSONResponse({"ok": False, "error": "invalid or revoked key"}, status_code=403)
    _touch_key(digest)
    return digest


BANK_VERSION = "1.0.0"

# Abuse guard: one key is one seat — a few machines and projects, not the
# internet. Distinct install_ids per key cap here. Updates reuse a known id and
# are never blocked; only brand-new installs over the cap are refused.
INSTALL_ID_CAP = 10


def _record_install(digest: str, iid: str, version: str) -> bool:
    """Track one install_id under its key. True when recorded, False when the key is over its cap."""
    try:
        db = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return True
    entry = db.get("keys", {}).get(digest)
    if entry is None:
        return True
    installs = entry.setdefault("installs", {})
    try:
        cap = int(entry.get("cap", INSTALL_ID_CAP))
    except (TypeError, ValueError):
        cap = INSTALL_ID_CAP
    if iid not in installs and len(installs) >= cap:
        return False
    installs[iid] = {"version": version, "at": datetime.now(timezone.utc).isoformat()}
    try:
        KEYS_FILE.write_text(json.dumps(db, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError:
        pass
    return True

INSTALL_PROMPT = (
    "Install the ai (愛) means love skill bank ({count} skills, bank {version}). Fetch {pack}. Then: "
    '0. Before fetching, GET https://aimeanslove.fyi/api/stats (open, no key) and compare its version to .agents/ailv.json. If equal, stop — you are current, nothing to download. '
    '1. Read .agents/ailv.json if it exists. If its bank equals "{version}", stop — already installed. '
    "2. List skill names already under .agents/skills/*/SKILL.md that the pack also contains. Keep those files; skip those ids — unification, never duplication. "
    "3. Write every other pack item to its file path. "
    "4. Generate one random install_id (a uuid), save it in .agents/ailv.json with the bank version, the ids written, and the ids skipped. Reuse the saved install_id on every update — one id per project, never per run. "
    "5. Work from local copies and never refetch mid-task. "
    "6. Report success: POST this JSON to https://aimeanslove.fyi/api/install/receipt?key=YOUR_KEY with the same key: "
    "{{\"version\": \"{version}\", \"install_id\": <your install_id>, \"installed\": <ids written>, \"kept\": <ids skipped>}}. "
    "If interrupted, re-run from the top — written files are skipped, nothing is lost."
)


def hit(route: str, skill: str | None = None) -> None:
    rollup_copies()
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


NAV_LINKS = [("/code", "Coding guide"), ("/ui", "UI guide"), ("/data", "Data guide"), ("/ops", "Ops guide"), ("/skills", "Skills"), ("/about", "About")]


def nav_link(href: str, label: str, active: str) -> str:
    current = ' aria-current="page"' if href == active else ""
    cls = "text-accent underline underline-offset-4" if href == active else "text-ink no-underline"
    return '<a href="' + href + '"' + current + ' class="' + cls + '">' + label + "</a>"


def library_uses() -> int:
    rollup_copies()
    routes = STATS["routes"]
    return routes.get("/board.json", 0) + routes.get("/api/skills", 0) + routes.get("/api/skill/:id", 0) + STATS.get("copies_applied", 0)


def nav(active: str) -> str:
    links = "".join(nav_link(href, label, active) for href, label in NAV_LINKS)
    return (
        '<nav class="topnav sticky top-0 z-10 border-b border-solid border-line" style="background:linear-gradient(rgba(255,255,255,0.92),rgba(255,255,255,0.86)),url(\'/brand/hero-mark.jpg\');background-size:cover;background-position:center;">'
        '<div class="max-w-[72ch] mx-auto px-4 py-3 text-center">'
        '<a href="/" class="font-mono font-bold text-lg md:text-xl inline-flex items-center justify-center gap-2 text-ink no-underline">'
        '<span>ai (<span class="text-accent" style="font-family:\'Klee One\',\'Hannotate SC\',\'Kaiti SC\',\'STKaiti\',\'KaiTi\',cursive;font-size:1.35em;line-height:1;">愛</span>) means love</span></a>'
        '<div class="mt-1.5 flex flex-wrap items-center justify-center gap-x-5 gap-y-1">' + links + "</div>"
        "</div></nav>"
    )


DOWNLOAD_ICON = '<i data-lucide="download" width="12" height="12" class="inline align-middle"></i>'


ISLAND_JS = """import {LitElement, html} from 'https://cdn.jsdelivr.net/npm/lit@3.3.3/+esm';
class UsesBadge extends LitElement {
  static properties = { uses: { type: Number } };
  createRenderRoot() { return this; }
  constructor() {
    super();
    this.uses = parseInt(this.getAttribute('start') || '0', 10);
  }
  connectedCallback() {
    super.connectedCallback();
    this._timer = setInterval(() => { if (!document.hidden) this._load(); }, 60000);
  }
  disconnectedCallback() {
    super.disconnectedCallback();
    clearInterval(this._timer);
  }
  async _load() {
    try {
      const r = await fetch('/api/stats');
      if (!r.ok) return;
      const j = await r.json();
      const t = (j.stats && j.stats.routes) || {};
      this.uses = (t['/board.json'] || 0) + (t['/api/skills'] || 0) + (t['/api/skill/:id'] || 0);
    } catch (e) { /* stay on last count */ }
  }
  updated() { if (window.lucide) window.lucide.createIcons(); }
  firstUpdated() { const f = this.querySelector('[data-fallback]'); if (f) f.remove(); }
  render() {
    return html`<a href="/#agent" class="font-mono text-xs bg-accent text-white rounded-full px-2.5 py-0.5 no-underline whitespace-nowrap">${this.uses} <i data-lucide="download" width="12" height="12" class="inline align-middle"></i></a>`;
  }
}
customElements.define('uses-badge', UsesBadge);"""


def float_pills() -> str:
    uses = library_uses()
    return (
        '<div class="mx-auto w-full max-w-[72ch] px-4 pt-3 flex items-center">'
        f'<uses-badge start="{uses}"><span data-fallback><a href="/#agent" class="font-mono text-xs bg-accent text-white rounded-full px-2.5 py-0.5 no-underline whitespace-nowrap">{uses} {DOWNLOAD_ICON}</a></span></uses-badge>'
        '<a href="/#support" data-open-support class="font-mono text-xs border border-solid border-accent text-accent rounded-full px-2.5 py-0.5 no-underline ml-auto">support us</a>'
        '<button type="button" data-open-contact class="font-mono text-xs border border-solid border-accent text-accent rounded-full px-2.5 py-0.5 ml-2 bg-transparent cursor-pointer">contact us</button>'
        "</div>"
    )


SUPPORT_DIALOG = """<dialog id="support-dialog" class="rounded-xl border border-solid border-line bg-white p-5 text-left text-ink max-w-[420px] backdrop:bg-ink/60">
<p class="font-display text-[22px] mb-3">Support the library</p>
<p class="m-0">Pay once, read forever: one $9.99 key unlocks the bank for your agents — up to 10 projects, free updates forever, no subscription. If these skills saved you tokens, chip in when donations open too — every bit keeps the lights on for the next agent. Donations are not open yet — check back soon.</p>
<div class="mt-3 text-right"><button type="button" data-close-support class="cursor-pointer border border-solid border-line bg-white rounded-lg px-3 py-1.5">Close</button></div>
</dialog>"""


FOOTER = (
    '<footer class="border-t border-solid border-line px-8 py-[18px] flex justify-center gap-x-6 gap-y-3 flex-wrap text-[13px] text-muted text-center">'
    '<a href="/about" class="text-accent underline">about</a>'
    '<a href="/#contact" data-open-contact class="text-accent underline">contact us</a>'
    "</footer>"
)


def page(title: str, desc: str, active: str, body: str, machine: str | None = None) -> str:
    tag = '<script type="application/json" id="machine">' + machine + "</script>" if machine else ""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        "<title>" + title + " — ai (愛) means love</title>\n"
        '<meta name="description" content="' + desc + '">\n'
        '<link rel="icon" type="image/png" href="/brand/favicon.png">\n'
        '<meta property="og:title" content="' + title + " — ai (愛) means love" + '">\n'
        '<meta property="og:description" content="' + desc + '">\n'
        '<meta property="og:image" content="' + SITE_URL + '/brand/og-card.png">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        + TAILWIND_HEAD
        + "</head>\n"
        '<body class="m-0 text-ink bg-paper font-sans flex flex-col min-h-screen">' + '<a href="#content" class="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-50 focus:bg-white focus:px-3 focus:py-2 focus:border focus:border-solid focus:border-line">Skip to content</a>' + nav(active) + float_pills() + '\n<main id="content" class="max-w-[72ch] w-full flex-1 mx-auto px-8 pt-8 pb-16 text-left">' + body + "</main>\n"
        + FOOTER + SUPPORT_DIALOG + contact_dialog() + "\n<script>" + CLIENT + "</script>\n" + '<script type="module">' + ISLAND_JS + "</script>\n" + tag + "</body></html>"
    )


HOME_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">ai (<span class="text-accent" style="font-family:'Klee One','Hannotate SC','Kaiti SC','STKaiti','KaiTi',cursive;font-size:1.2em;line-height:1;">愛</span>) means love</h1><p class="text-[17px] max-w-[72ch]">New here? <a href="#manifesto" class="text-accent underline">Read the manifesto</a> first — four short points that explain the whole idea. Then pick a guide: the <a href="/code" class="text-accent underline">coding guide</a>, the <a href="/ui" class="text-accent underline">UI guide</a>, the <a href="/data" class="text-accent underline">data guide</a>, the <a href="/ops" class="text-accent underline">ops guide</a>, or <a href="/skills" class="text-accent underline">skills</a> for your agent.</p></header>
<section id="manifesto" class="mt-10 border-t-0 pt-0 space-y-3">
<h2 class="font-display text-[22px] mb-3">Manifesto</h2>
<ol class="text-left space-y-3.5 list-decimal pl-6 max-w-[72ch]">
<li><strong>Build for the reader that matters.</strong> The reader is an agent, not a person. Short modules, explicit I/O, JSON-first data, tables over prose.</li>
<li><strong>Tokens are the budget.</strong> Every abstraction, adjective, and clever trick is a token tax on every future read. Plain beats clever.</li>
<li><strong>Humans give verdicts, not line reviews.</strong> Working = tests pass. Desirable = screenshot looks right. Nobody needs to admire the source.</li>
<li><strong>Guides must be fetchable.</strong> UI rules, code rules, and checks live behind one open endpoint, copy-pasteable into any agent session. Free forever.</li>
</ol>
</section>
<section class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">The old way and the new way</h2>
<p>Every page on this site makes one argument. The old way optimized for human readers and human operators. The new way — agentic ops — optimizes for agent builders and agent operators, with humans judging only outcomes.</p>
<div class="grid gap-4 my-6">
<div class="space-y-2"><h3 class="text-[19px] font-bold">The old way — built for humans</h3><p>Code was written so humans could read and manage it. One big framework did everything: Django, Rails, Laravel — one way of doing things, one manual to read. Interfaces were hand-built, pixel by pixel. Systems shipped by hand: SSH, console clicks, deploys on Fridays nobody fully understood. When things broke, a hero got paged with no notes. Audits were screenshots taken the week before.</p></div>
<div class="space-y-2"><h3 class="text-[19px] font-bold">The new way — agentic ops</h3><p>AI writes most of the code now, so code is written for agents to read: explicit, grouped by feature, managed through skills and context. The engineer is the driver — they point, the AI builds. Interfaces assemble from stocked pieces, and humans judge the screenshot. Systems ship through gated pipelines the agent runs: previewed, health-checked, reversible with one action. Pages carry runbooks and trigger events, so agents acknowledge and roll back without parsing human text. Evidence collects itself continuously. Humans verify five things: tests pass, the screen looks right, the dashboard is green, the drill record exists, and a named human owns the blast radius — and nothing else.</p></div>
</div>
<p>Industry zombies shamble on: MVC, MVP, and layered architectures were fences so human teams could share code without colliding. One agent doesn't need the fences — it sees the whole flow at once. But teams of agents still need to stay out of each other's way, so the contract replaces the layer: shared models, tests at the seams, features grouped together. Write code that lets agent teams work together, not human teams.</p>
</section>
<section class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">Proof, measured</h2>
<p>A typical task pack reads about 2.2 to 2.8 thousand tokens — 13 to 17 percent of the 23.0k-token bank — because the agent fetches matched skills only, never the whole bank. Counted by our own self-test (<code class="font-mono text-[13px]">script/bench.py</code>), same method as the card badges. The full with/without trial — matched pack versus whole bank versus no skills, scored on tokens, wall time, and defects — is the <code class="font-mono text-[13px]">verify-benchmark</code> protocol: run it, publish method plus raw numbers, or the claim is marketing.</p>
<p>First trial, run November 2026: three design tasks (webhook receiver, evolution-proof validation, stateful rollout) × bare versus skill-fed agents. Defects: 0 and 0 on all three — the model already knows industry doctrine, so skills didn't change correctness here. Outputs ran 136–289 tokens in both arms. What the pack arms added was completeness: freshness SLAs, external probes, deploy receipts — house specifics, not textbook recall. The trial that should discriminate is a coordination-heavy build, not doctrine recall; that run is open. Whole-bank arm not run: feeding all 102 skills to test recall nobody disputes would be cost without a question.</p>
</section>
<section class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">Pay once, use forever</h2>
<p>One $9.99 payment gets you a key to the whole bank — all 104 skills, every future update, no subscription, no meter. One seat covers up to 10 projects with free updates forever — teams buy a key per engineer.</p> A typical task reads about 2.4k tokens instead of the 23.0k bank: pennies per task at current API rates, against a single payment that never renews. Keys open soon — the skill endpoints already check for one, and until checkout opens everything stays readable on the <a href="/skills" class="text-accent underline">skills page</a>.</p>
</section>
<section id="agent" class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">Give this to your agent</h2>
<p>Have a key? One call installs the whole bank — the agent fetches, writes one file per skill, and works from local copies:</p>
<pre class="bg-ink text-white rounded-lg p-3.5 text-sm overflow-auto text-left">curl "https://aimeanslove.fyi/api/install?key=YOUR_KEY"</pre>
<p class="bg-wash rounded-lg p-2.5 text-sm text-left">Copy-paste install prompt — swap in the key, hand the whole block to the agent:</p>
<pre class="bg-ink text-white rounded-lg p-3.5 text-sm overflow-auto text-left">Install the ai (愛) means love skill bank (104 skills, bank 1.0.0). Fetch https://aimeanslove.fyi/api/install?key=YOUR_KEY. Then: 0. Before fetching, GET https://aimeanslove.fyi/api/stats (open, no key) and compare its version to .agents/ailv.json. If equal, stop — you are current, nothing to download. 1. Read .agents/ailv.json if it exists. If its bank equals "1.0.0", stop — already installed. 2. List skill names already under .agents/skills/*/SKILL.md that the pack also contains. Keep those files; skip those ids — unification, never duplication. 3. Write every other pack item to its file path. 4. Write .agents/ailv.json with the bank version, the ids written, and the ids skipped. 5. Work from local copies and never refetch mid-task. 6. Report success: POST {"version": "1.0.0", "installed": [...], "kept": [...]} to https://aimeanslove.fyi/api/install/receipt?key=YOUR_KEY with the same key. If interrupted, re-run from the top — written files are skipped, nothing is lost.</pre>
<p>No key yet? Taste free — every prompt is readable on the <a href="/skills" class="text-accent underline">skills page</a>, and the field list plus usage stats stay open:</p>
<pre class="bg-ink text-white rounded-lg p-3.5 text-sm overflow-auto text-left">curl https://aimeanslove.fyi/api/fields</pre>
</section>"""

UI_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">UI guide</h1><p class="text-[17px] max-w-[72ch]">Goal: an agent builds the drafts fast; a human shapes feel in the middle and confirms at the end. Mobile-first always — 360px first, scale up — unless the task genuinely needs a full monitor. Semantic HTML, tokens not prose, every state visible as text.</p></header>
<section class="grid gap-4 my-6">
<div class="border border-solid border-line rounded-xl p-5 bg-white"><h2 class="font-display text-[22px] mb-3">1 · Structure</h2><ul class="text-left space-y-2 list-disc pl-5">
<li>Semantic landmarks: <code class="font-mono text-[13px]">&lt;header&gt; &lt;main&gt; &lt;footer&gt;</code>, real <code class="font-mono text-[13px]">&lt;button&gt;</code>/<code class="font-mono text-[13px]">&lt;a&gt;</code>/<code class="font-mono text-[13px]">&lt;input&gt;</code> with visible labels. No div-buttons.</li>
<li>Icon-only controls welcome — but every control exposes metadata: a real element, a label or <code class="font-mono text-[13px]">aria-label</code>, and a <code class="font-mono text-[13px]">data-action</code>. Humans get the pixels; agents read the metadata.</li>
<li>Shape every script your readers use. System fonts usually cover complex scripts on modern phones — verify on a real device, since shaping bugs only show in real rendering.</li>
<li>Icons come from Lucide (<a href="https://lucide.dev/" target="_blank" rel="noopener" class="text-accent underline">Lucide</a>) — the best set for agents — never hand-written. Write <code class="font-mono text-[13px]">&lt;i data-lucide="name"&gt;</code> plus one <code class="font-mono text-[13px]">lucide.createIcons()</code> call — the agent picks names from the set, nobody draws pixels or pastes SVG paths by hand. Drawing icons burns tokens and time for a worse result: Lucide is already trained into the model, so the agent knows every name, and already familiar to users, so people recognize each icon on sight.</li>
<li>Tailwind utilities for layout. System font stack.</li>
<li>Flexbox for page and component layout — one direction at a time, same pattern on every page, so agents learn it once. The shell is a flex column: <code class="font-mono text-[13px]">body.flex.flex-col.min-h-screen</code>, content <code class="font-mono text-[13px]">main.flex-1</code> grows, footer sits last. Short pages get whitespace in the content area, never a floating footer — the footer is always stuck to the bottom.</li>
<li>One content width per page for components. Every block — cards, sections, banners — spans the same width, so nothing looks narrower than its neighbor. Only break this when the engineer decides it on purpose, for example a form that should stay small on desktop.</li>
<li>Running prose is the exception: cap it at 45–75 characters per line, about 66 ideal — longer lines get skipped, not read (<a href="https://www.baymard.com/blog/line-length-readability" target="_blank" rel="noopener" class="text-accent underline">Baymard</a>, <a href="https://practicaltypography.com/line-length.html" target="_blank" rel="noopener" class="text-accent underline">Butterick</a>, WCAG caps blocks at 80).</li>
<li>Be findable. One H1, a plain-words title and description, real links, a sitemap that lists every page, and topics checked on Google Trends before they are built — humans arrive through search, agents through the map. See the <code class="font-mono text-[13px]">ui-seo</code> skill.</li>
<li>Fast by budget. Set a budget (page weight, endpoint milliseconds, query count), measure first, cache the repeats, shrink the payload, and re-measure after every change. See the <code class="font-mono text-[13px]">code-perf</code> skill.</li>
<li>Shed load, keep serving. Rank features by criticality, shed the nice-to-haves behind flags, and prove the degraded mode with a stress test — feature grouping means a future service split follows existing seams. See the <code class="font-mono text-[13px]">code-fallback</code> skill.</li>
<li>External links open a new tab. Any link leaving the site gets <code class="font-mono text-[13px]">target="_blank" rel="noopener"</code> so the reader never loses their place here; internal links never do.</li></ul></div>
<div class="border border-solid border-line rounded-xl p-5 bg-white"><h2 class="font-display text-[22px] mb-3">2 · Styling tokens + Tailwind</h2><ul class="text-left space-y-2 list-disc pl-5">
<li><a href="https://tailwindcss.com/" target="_blank" rel="noopener" class="text-accent underline">Tailwind</a> utilities for layout and spacing, on top of three color tokens (<code class="font-mono text-[13px]">--ink --paper --accent</code>) and a <code class="font-mono text-[13px]">4/8/16/32</code> scale. Preflight stays on as the consistent baseline — every margin, bullet, and underline is stated explicitly, never inherited from a browser default.</li>
<li>Two neutrals + one accent. 1px solid lines. Radii: 6px / 10px. Utilities handle the how, tokens handle the what.</li>
<li>Minimalist palettes win. Studies find 1–2 dominant colors plus functional neutrals complete tasks about 15% faster with about 25% fewer errors than vibrant multi-color themes — saturated color everywhere is visual overload (<a href="https://www.ijahci.com/index.php/ijahci/article/download/21/17/31" target="_blank" rel="noopener" class="text-accent underline">IJAHCI study</a>). Our two-neutrals-plus-accent is that finding, applied.</li>
<li>Colors must mean what people expect. Green confirms, red destroys or errors, blue informs — matched expectations beat clever recoloring, and even plain grayscale beats illogical color (<a href="https://academicjournals.org/journal/JECI/article-full-text/61BAE8470266" target="_blank" rel="noopener" class="text-accent underline">JECI study</a>). Never subvert these; reserve the accent for brand and calls to action.</li>
<li>Contrast by ratio: 60-30-10. Roughly 60% neutral background, 30% secondary structure and text, 10% high-contrast accent on interactive elements only — and body text holds 4.5:1 contrast or better. Balanced warm-cool pairings build trust; the ratio is what makes key elements instant to find (<a href="https://journal.pandawan.id/b-front/article/download/1057/775/6397" target="_blank" rel="noopener" class="text-accent underline">B-Front study</a>).</li>
<li>Color moves money across cultures. About 44% of consumers say the palette influenced a purchase, and blue tests well in every region studied — so the accent earns its keep twice: brand and conversion (<a href="https://doi.org/10.47909/awari.744" target="_blank" rel="noopener" class="text-accent underline">Alotaibi 2025</a>).</li>
<li>Interactive components come from Flowbite (<a href="https://flowbite.com/" target="_blank" rel="noopener" class="text-accent underline">Flowbite</a>), never hand-built. Flowbite is made for Tailwind and mobile-first, and loads from one CDN script with no build step. Nav links stay visible on every breakpoint — hidden menus roughly halve discoverability, so the hamburger stays off. Reach for the library when you need a dropdown, modal, or drawer instead of hand-building one.</li>
<li>No gradients, no glass blur, no gray-on-gray body text. Contrast ≥ 4.5:1.</li></ul></div>
<div class="border border-solid border-line rounded-xl p-5 bg-white"><h2 class="font-display text-[22px] mb-3">3 · Behavior</h2><ul class="text-left space-y-2 list-disc pl-5">
<li>Every mutation exposes <code class="font-mono text-[13px]">idle → working → done | error</code> as text, never color alone.</li>
<li>Confirm destructive actions inline. Honor <code class="font-mono text-[13px]">prefers-reduced-motion</code>.</li>
<li>Seed demo data: no lorem, no empty lists. Each screen lists 3 things to eyeball.</li>
<li>Verification screenshots live in the project's <code class="font-mono text-[13px]">shots/</code> folder (gitignored), named for what they show — never <code class="font-mono text-[13px]">/tmp</code>, so they don't pile up where nobody looks.</li>
<li>Never trust a headless screenshot alone. Headless renders can lie — missing styles, shifted layout — while a real browser shows the truth. Use headless for a quick first look only; proof is a real browser, or the user's own screenshot. When the two disagree, believe the user's screen and stop editing until you know what it actually shows.</li>
<li>Layout follows the published rulebook. <a href="https://www.w3.org/TR/WCAG21/#reflow" target="_blank" rel="noopener" class="text-accent underline">WCAG 2.1 Reflow (1.4.10)</a> is the standard: content usable with no loss and no two-dimensional scrolling — the exceptions (tables, maps, diagrams) scroll inside their own component, never the page. Alignment beyond that is measured, not eyeballed. See the verify-layout skill.</li></ul></div>
<div class="border border-solid border-line rounded-xl p-5 bg-white"><h2 class="font-display text-[22px] mb-3">4 · Components</h2><ul class="text-left space-y-2 list-disc pl-5">
<li>Short lists get radios. For 2 to 4 options use radio buttons or segmented controls — everything visible, one click to answer; dropdowns hide choices and cost clicks, with higher non-response and longer times (<a href="https://journals.sagepub.com/doi/10.1177/0894439306293888" target="_blank" rel="noopener" class="text-accent underline">Healey 2007</a>). Dropdowns only for 5 to 10 familiar options.</li>
<li>Long lists get filters or plain inputs. Past about 15 items use a combo box — live filtering beats scrolling; for familiar data like birth years a plain numeric input beats any list (<a href="https://designnotes.blog.gov.uk/2013/12/05/asking-for-a-date-of-birth/" target="_blank" rel="noopener" class="text-accent underline">GOV.UK study</a>). Never make users scroll 50+ items.</li>
<li>Hover menus wait. Desktop hover menus open after a 300–500ms delay so passing cursors don't flicker them shut (<a href="https://baymard.com/research-articles/dropdown-menu-flickering-issue" target="_blank" rel="noopener" class="text-accent underline">Baymard</a>); click-to-open is always safe.</li></ul></div>
</section>
<section class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">
<h2 class="font-display text-[22px] mb-3">5 · Images</h2>
<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Every image earns its place.</strong> Above the fold carries one value headline, one supporting line, one primary action, one visual, one trust signal — clear beats clever, and five-plus competing links sink conversion (<a href="https://ivyforms.com/blog/hero-section-examples/" target="_blank" rel="noopener" class="text-accent underline">Unbounce benchmarks via IvyForms</a>). Stores with a clear value proposition convert 2–4x higher (<a href="https://webmedic.com/ecommerce-value-proposition" target="_blank" rel="noopener" class="text-accent underline">MarketingSherpa via WebMedic</a>).</li>
<li><strong>The hero is usually the slowest thing.</strong> Most mobile largest-paint elements are images (<a href="https://isitdownorjustme.net/web/website-imagery-optimization-guide/" target="_blank" rel="noopener" class="text-accent underline">Core Web Vitals data</a>), so treat the above-fold image as a budget: eager-load with high fetch priority, lazy-load everything below, modern formats, source sets with sizes, explicit width and height so layout never shifts (<a href="https://dev.to/ashtech52/core-web-vitals-in-2026-how-to-improve-lcp-inp-and-cls-on-slow-pages-2514" target="_blank" rel="noopener" class="text-accent underline">Core Web Vitals 2026</a>).</li>
<li><strong>Say what it is, or say nothing.</strong> Informative images get real alt text; decorative and structural art gets empty alt or becomes a background. See the <code class="font-mono text-[13px]">ui-images</code> skill.</li></ul>
</section>
<section class="mt-4 bg-wash border border-solid border-line rounded-xl p-5 space-y-3"><h2 class="font-display text-[22px] mb-3">Client state — for hands, not data</h2>
<p>Typing, dragging, and drawing are faster than any round trip, so they live in the browser: a small isolated interactive region — called an "island" — holds the work-in-progress. The pattern comes from <a href="https://jasonformat.com/islands-architecture/" target="_blank" rel="noopener" class="text-accent underline">Islands Architecture (Jason Miller; term coined by Katie Sylor-Miller at Etsy)</a>: server HTML with interactive regions hydrated in place, instead of one app-wide runtime. Islands are Lit custom elements from the start (<a href="https://lit.dev/" target="_blank" rel="noopener" class="text-accent underline">Lit</a>), loaded from the pinned CDN module with no build step. Most sites are apps now, so one way beats two: no Alpine-first ladder to climb. But the server still owns the shared truth. The rule: never keep the same fact in both places without an expiry — sync back on natural pauses (debounced save), and the server re-checks everything it receives, because browser state is never trusted.</p>
<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Browser holds:</strong> keystrokes, drag positions, drawing strokes, open tabs, form drafts — anything hands are doing right now, plus prefs and anything that must work offline.</li>
<li><strong>Server holds:</strong> everything shared, saved, or shown to anyone else. When in doubt, the server wins.</li>
<li><strong>No global store by default.</strong> A Pinia/Zustand-style store is a second copy of the truth that needs syncing and goes stale. Small local islands don't have that problem because they own nothing shared.</li>
<li><strong>When an island earns its place.</strong> Most pages need none — server HTML is cheaper to write and cheaper for agents to read. Build one when the region must respond faster than a round trip: typing, dragging, live numbers, offline drafts. Our own usage badge is one: it re-reads the stats every minute without a reload.</li>
<li><strong>Light DOM, always.</strong> Our islands render into the light DOM (never shadow), so Tailwind utilities and Lucide icons keep working inside them with no shadow styling to fight. HTMX never targets an island or anything inside one — Lit owns its element's children.</li></ul></section>
<section class="mt-4 bg-wash border border-solid border-line rounded-xl p-5 space-y-3"><h2 class="font-display text-[22px] mb-3">Mobile track — one language to both app stores</h2>
<p>For app-like mobile builds, the token-densest path is <strong>FastAPI + <a href="https://htmx.org/" target="_blank" rel="noopener" class="text-accent underline">HTMX</a> + Tailwind, wrapped with <a href="https://capacitorjs.com/" target="_blank" rel="noopener" class="text-accent underline">Capacitor</a></strong>. One language (Python) serves logic and layout; almost no JavaScript is written; no Swift, Kotlin, or Dart is touched. Honest version of the pitch: HTMX doesn't delete data-fetching tokens, it moves them — fragments over JSON means no client state to synchronize, and that's where the savings actually come from. Tailwind's edge is correctness speed (models know it cold), not byte count — long class strings cost tokens per element, so keep components small.</p>
<div class="grid gap-4 my-6 text-left">
<div class="space-y-2"><h3 class="text-[19px] font-bold">FastAPI serves HTML</h3><p>Routes return fragments, not JSON. No fetch calls, no serializers, no client router drifting out of sync.</p></div>
<div class="space-y-2"><h3 class="text-[19px] font-bold">HTMX for interactivity</h3><p><code class="font-mono text-[13px]">hx-get="/profile" hx-target="#content"</code> gives SPA behavior in one attribute. No React, no Vue, no state store. Boundary rule: HTMX swaps page-level regions; Lit owns its element's children — never aim <code class="font-mono text-[13px]">hx-target</code> at or into an island.</p></div>
<div class="space-y-2"><h3 class="text-[19px] font-bold">Tailwind + Capacitor</h3><p>Responsive layout inline (<code class="font-mono text-[13px]">flex md:flex-row flex-col</code>), no stylesheet context-switching. Capacitor wraps the finished mobile viewport into iOS/Android shells; native features via plugins.</p></div>
</div>
</section>"""

def details_card(title: str, inner: str, is_open: bool = False, anchor: str | None = None) -> str:
    """One shared collapsible card. Reuse this; never hand-write another."""
    attrs = ""
    if anchor:
        attrs += ' id="' + anchor + '"'
    if is_open:
        attrs += " open"
    return (
        '<details class="border border-solid border-line rounded-xl p-5 bg-white text-left space-y-2"' + attrs + ">"
        '<summary class="cursor-pointer list-none flex items-center justify-between gap-3 [&::-webkit-details-marker]:hidden">'
        '<h2 class="font-display text-[22px] text-left">' + title + "</h2>"
        '<span aria-hidden="true" class="open:rotate-180 motion-safe:transition-transform text-accent text-xl leading-none shrink-0">\u25be</span></summary>'
        + inner + "</details>"
    )


CODE_BODY = ("""<header class="space-y-2"><h1 class="font-display text-[38px]">Coding guide</h1><p>This guide backs you up while you build. Two rules cover nearly everything: <strong>write Python, because agents generate it fastest</strong> — and <strong>lean on guardrail frameworks, because they make whole classes of mistakes unwritable</strong>. Everything below is support, not ceremony.</p></header>
<section class="grid gap-2 my-4">
"""
    + details_card("1 · Python first", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>AI writes Python best.</strong> AI models have read more Python than any other language, so they make fewer mistakes in it. Python also uses few special symbols, so the same idea costs fewer tokens. That is a house position from building with agents, and the language reference is the backstop (<a href="https://docs.python.org/3/" target="_blank" rel="noopener" class="text-accent underline">Python docs</a>) — the guardrails below assume it.</li>
<li><strong>Type hints do real work.</strong> A type hint says what shape your data is, like <code class="font-mono text-[13px]">name: str</code>. The tools below read these hints and check your code for you, for free.</li>
<li><strong>One language for everything.</strong> Use Python for the server, for small scripts, and for command line tools. One language means less switching between tools and no extra code just to connect things.</li>
<li><strong>Python is the default, not the law.</strong> A few jobs need other tools — see <a href="#limits" class="text-accent underline">4 · Limits</a>. Everywhere else, Python.</li></ul>""",
        is_open=True,
    ) + "\n"
    + details_card("2 · Guardrails", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>FastAPI + Pydantic — because one declaration replaces three hand-written systems.</strong> You describe your data one time, in one class — and that class <em>is</em> the validator, the serializer, and the API documentation (<a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener" class="text-accent underline">FastAPI</a>, <a href="https://docs.pydantic.dev/" target="_blank" rel="noopener" class="text-accent underline">Pydantic</a>). Those three are exactly where agents invent inconsistent behavior when they write them by hand: a check Flask never had, an error message that lies, docs that drift from the code. Flask leaves all three to you; Django brings a whole system the agent must learn per task. FastAPI needs only your data class.</li>
<li><strong>SQLModel — because two matching copies is where drift bugs live.</strong> One class describes both your database table and your API data (<a href="https://sqlmodel.tiangolo.com/" target="_blank" rel="noopener" class="text-accent underline">SQLModel</a>), so disagreement is impossible by construction. The old way needs a table class plus a matching API class, and the bug always hides in the gap between them.</li>
<li><strong>Typer — because the function signature already describes the tool.</strong> Write a normal Python function and add one line on top of it (<a href="https://typer.tiangolo.com/" target="_blank" rel="noopener" class="text-accent underline">Typer</a>); types become options, the docstring becomes help. Argparse forces you to describe every option a second time by hand, and the two descriptions drift. One source, zero drift.</li>
<li><strong>gRPC between services — because polyglot teams need one contract, not one per language.</strong> When Python isn't everywhere, a single <code class="font-mono text-[13px]">.proto</code> file generates type-safe clients and servers in every language (<a href="https://grpc.io/" target="_blank" rel="noopener" class="text-accent underline">gRPC</a>), so Go, Java, and Python are guaranteed to agree on the wire format instead of each re-describing the API. Inside Python-only systems, reuse the same Pydantic models as the contract — no extra framework needed. Keep FastAPI at the edge facing users and agents, where humans and machines read JSON.</li>
<li><strong>Auth — sessions, OAuth, and passwords done once, rightly.</strong> Logins use signed cookies (built into Starlette — one secret key, no extra package). "Sign in with Google" uses <code class="font-mono text-[13px]">authlib</code>. Services talking to each other use JWTs via <code class="font-mono text-[13px]">pyjwt</code>. Passwords are checked with bcrypt via <code class="font-mono text-[13px]">passlib</code> — never write your own password check, because a wrong one fails silently and an agent will not notice.</li>
<li><strong>Background work — not inside the request.</strong> A web request should answer fast and finish. Fire-and-forget jobs (welcome emails) go in FastAPI <code class="font-mono text-[13px]">BackgroundTasks</code>. Real queues and schedules (video processing, nightly reports) go in a job runner like <code class="font-mono text-[13px]">arq</code>. The user never waits for work they cannot see.</li>
<li><strong>Migrations — not create-all.</strong> Databases change shape over time. <code class="font-mono text-[13px]">Alembic</code> applies each change as a small step, forward and back. Never use <code class="font-mono text-[13px]">create_all</code> on a live database — it rebuilds tables from scratch and real data disappears on redeploy.</li>
<li><strong>Lit — for pieces you build yourself, not pieces you borrow.</strong> Most builds today are apps. If yours is — an editor, a dashboard, a drawing tool — skip the HTML-first ladder and start with Lit islands or Lit throughout, over a CDN import map with no build step (<a href="https://lit.dev/" target="_blank" rel="noopener" class="text-accent underline">Lit</a>). Same FastAPI server behind them either way. Know what Lit is not: it gives you the machinery to build components, but ships zero ready-made ones — no menu, no dialog, no dropdown. Keep Flowbite for ready-made pieces; never rebuild one in Lit just to own it. If a Lit island itself needs ready-made pieces, use WebAwesome (Shoelace) over CDN — same no-build pattern, not a second design system to invent. And never React or Angular: they need a build step, ship heavy JavaScript, and cost tokens on every read — the opposite of this stack.</li>
<li><strong>Tailwind — not hand-written CSS.</strong> Never write stylesheets by hand. Hand-written CSS costs tokens twice: once to write, and again for every agent that must read it. Style with Tailwind utilities on top of three color tokens (<a href="https://tailwindcss.com/" target="_blank" rel="noopener" class="text-accent underline">Tailwind</a>); preflight stays on as the consistent baseline, every margin and bullet stated explicitly. Styling is the framework's job, not yours.</li>
<li><strong>Capacitor — not React Native, Flutter, or native code.</strong> Those are whole new languages and systems the agent must learn, and native apps need Swift or Kotlin. Capacitor takes the mobile web page you already built and wraps it for both app stores (<a href="https://capacitorjs.com/" target="_blank" rel="noopener" class="text-accent underline">Capacitor</a>), and ready-made plugins cover the common phone features (camera, location, push messages, files). Store risk is real: Apple has rejected bare wrapped web views under guideline 4.2 — ship with device features engaged, not a bare wrapper.</li> The caveat: if you need a phone feature with no ready-made plugin, you write one small bridge piece — not a whole native app. A few things still need real native code: games and heavy graphics, home-screen widgets and Live Activities, watch apps, music apps where sound delay matters, and brand-new phone features with no plugin yet. Typical business and content apps never touch these.</li>
<li><strong>Throttle expensive endpoints.</strong> Public APIs, forms, and beacons get a per-IP sliding window with a <code class="font-mono text-[13px]">429</code> plus <code class="font-mono text-[13px]">Retry-After</code> answer when over limit — limits live in config, not code. See the <code class="font-mono text-[13px]">code-ratelimit</code> skill.</li>
<li><strong>Framework first, hand-written last.</strong> If the stack already solves it — layout, icons, menus, validation — use the stack's piece, never your own version. We lost days rebuilding a mobile menu by hand; the library version worked the first time. Hand-write only what no framework covers, like a single HTTP header.</li></ul>""") + "\n"
    + details_card("3 · Shape &amp; proof", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Small, flat modules.</strong> Keep each file small: one job, under 150 lines. A small file fits in the AI's memory at one time. Write flat code: check for problems first and exit early, so the reader follows one straight path. When something goes wrong, send a clear error answer — never a crash report.</li>
<li><strong>Check input at the door.</strong> When data comes in, check three things: is it the right type, the right size, and on the allowed list? Say no to files that are too big before you open them. Keep passwords and keys in environment variables, never in code or logs — code and logs get copied and shared, and secrets would leak.</li>
<li><strong>Tests are the review.</strong> No person reads your code to judge it. Instead, write one small test for each thing your code does, then run the tests. Green means it works. Red means it is broken. That is the whole review.</li>
<li><strong>Layers like MVC were fences for human teams.</strong> MVC and Model-View-Presenter split code so many people could work without breaking each other's parts. One agent doesn't need those fences — it sees the whole flow at once, and every fence is extra code it must read. Keep a boundary only when something real enforces it: different trust (browser vs server), different machines, or different people.</li>
<li><strong>More humans still means more boundaries.</strong> When several people with agents build together, the collision is real: two agents editing the same file, contradictory fixes, broken merges. Keep component boundaries plus written contracts — shared Pydantic models, tests at the seams — so parallel work doesn't collide. The contract does the coordinating, not the layers.</li>
<li><strong>Some skills are always on.</strong> <code class="font-mono text-[13px]">code-secure</code>, <code class="font-mono text-[13px]">code-reuse</code>, and <code class="font-mono text-[13px]">code-token</code> apply to almost every task — read those three every time, then let the index skill match the rest to the task. Never skip the always-on three to save tokens; they are what keep every task safe, shared, and cheap.</li>
<li><strong>Disclose progressively.</strong> This bank follows <a href="https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills" target="_blank" rel="noopener" class="text-accent underline">progressive disclosure, the Agent Skills model</a>: the agent reads the map first, then only the details its task needs. The <code class="font-mono text-[13px]">code-index</code> skill is the map, three skills are always on, the rest load only on a match. Small skills stay small because the map carries the routing — and references flow downward only, a rule the test suite enforces, so the map can never loop back on itself.</li>
<li><strong>Where it lives.</strong> The <a href="/skills" class="text-accent underline">skills page</a> shows every skill with its why-line plus the machine doors agents fetch through. Install once from the skills page, then read locally — never fetch per task.</li>
<li><strong>Drop the layers, keep the grouping.</strong> Group by feature, not by layer: a component's files sit together — <code class="font-mono text-[13px]">checkout_routes.py</code>, <code class="font-mono text-[13px]">checkout_models.py</code>, <code class="font-mono text-[13px]">checkout_tests.py</code> — named <code class="font-mono text-[13px]">&lt;feature&gt;_&lt;kind&gt;</code> so the next agent finds everything in one place. But if the codebase you are working in already uses a pattern like MVC, follow that pattern instead: restructuring working code costs tokens and every move risks new errors. Match the house style; save rewrites for when a real force demands them.</li></ul>""",
        is_open=True,
        anchor="shape-proof",
    ) + "\n"
    + details_card("4 · Limits", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Heavy math (video, AI number-crunching).</strong> Python uses one core per process. Let other tools do the math, or run more servers — Python gives the orders.</li>
<li><strong>Answers needed in single-digit milliseconds</strong> (trading, live bidding, game server ticks). Use Go or Rust.</li>
<li><strong>Over 100,000 live connections at once</strong> (huge chat, live tracking). Erlang and Elixir were built for exactly this.</li>
<li><strong>Functions that sleep most of the time and must wake instantly</strong> (spiky serverless). Python wakes slowly; Go and Rust wake fast.</li>
<li><strong>Tiny computers with no operating system.</strong> Use C or Rust.</li>
<li><strong>Apps that must work fully offline with heavy local logic.</strong> That needs real code on the device, not pieces from a server.</li></ul>""",
        anchor="limits",
    ) + "\n"
    + """</section>
"""
)

DATA_BODY = ("""<header class="space-y-2"><h1 class="font-display text-[38px]">Data guide</h1><p class="text-[17px] max-w-[72ch]">Data an agent can trust. Every dataset reproducible from its inputs; every event counted exactly once. Humans judge the dashboard numbers, never the pipeline code.</p></header>
<p class="text-left mt-4"><strong>The old way</strong> designed data for human eyes: charts to understand it, CSVs to inspect it, humans reading graphs to decide. <strong>The new way</strong> feeds raw events and tables to agents that never need a picture — collection is at-least-once plus dedup everywhere, storage is queried rather than browsed, manipulation is tested transforms over partitions. Visualization stays, but its job changed: charts are the human verdict layer, not the analysis. Chart choice follows a measured ranking, not taste — position beats length beats angle beats area beats color (<a href="https://www.textbookofusability.com/people/william-cleveland.html" target="_blank" rel="noopener" class="text-accent underline">Cleveland &amp; McGill, 1984</a>), which is why bars beat pies. And every chart ships a machine twin: the data table the <a href="https://www.w3.org/WAI/WCAG22/Techniques/general/G92.html" target="_blank" rel="noopener" class="text-accent underline">W3C prescribes</a> plus, when interactive, a declarative <a href="https://vega.github.io/vega-lite/" target="_blank" rel="noopener" class="text-accent underline">Vega-Lite-style spec</a> — so agents judge and rebuild from data, never pixels. Movement is agent work; meaning stays human — what counts as active or revenue is decided by people, then defined once for every dashboard to share. See the <code class="font-mono text-[13px]">ui-charts</code> and <code class="font-mono text-[13px]">ui-chart-twin</code> and <code class="font-mono text-[13px]">data-metrics</code> skills.</p>
<section class="grid gap-2 my-4">
"""
    + details_card("1 · Land once", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Every event lands exactly once.</strong> Producers attach an idempotency key and retry freely; consumers dedup on that key before writing, so replays converge instead of double-counting (<a href="https://kafka.apache.org/documentation/" target="_blank" rel="noopener" class="text-accent underline">Kafka's exactly-once semantics</a> work the same way: retries are safe only when the consumer dedupes). Retries without dedup keys inflate everything downstream — revenue, usage, analytics. See the <code class="font-mono text-[13px]">data-ingest</code> skill.</li>
<li><strong>Schema first, poison last.</strong> Validate against the schema on arrival and reject unknown fields loudly — never silently drop. Poison events go to a dead-letter queue after N tries and page nobody; the stream never blocks on one bad record, and the dedup store stays bounded with a TTL past the retry window.</li></ul>""",
        is_open=True,
    ) + "\n"
    + details_card("2 · Move in order", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Pipelines are DAGs, not cron chains.</strong> Model every pipeline with explicit dependencies, per-task retries with backoff, and a stall SLA that pages when breached — success stays quiet. Chained cron fails silently at 3am; explicit deps fail loudly with an owner. See the <code class="font-mono text-[13px]">data-orchestrate</code> skill.</li>
<li><strong>Batch work reloads by partition.</strong> Transforms live in tested code, and rerunning a date range converges instead of duplicating. Backfills touch bounded partitions, throttled below production priority — never full-table reruns that overload sources or double-write. See the <code class="font-mono text-[13px]">data-etl</code> and <code class="font-mono text-[13px]">data-backfill</code> skills.</li>
<li><strong>Concurrent writers converge, never clobber.</strong> Multi-record changes go in one transaction; contested rows use optimistic locking with retry, never held locks; hot rows shard instead of serializing. The database remains the adult in the room — its constraints beat application checks that race. Old systems hand-tuned locks in app code; the new rule is simpler: transact by default, escalate only what proves it needs more. See the <code class="font-mono text-[13px]">data-concurrency</code> skill.</li></ul>""") + "\n"
    + details_card("3 · Trust but verify", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Contracts evolve additively.</strong> Version every event and table schema in one registry with compatibility checks; additive changes only, consumers pinning the version they read. A breaking rename with no contract silently breaks every downstream reader. See the <code class="font-mono text-[13px]">data-contracts</code> skill.</li>
<li><strong>Gate promotion on signals, not row counts.</strong> Freshness, nulls, volume, and distribution — row counts pass plausible-but-wrong data. Failing checks block the pipeline with the offending sample attached, and quality history per dataset turns sudden shifts into incidents. See the <code class="font-mono text-[13px]">data-quality</code> skill.</li>
<li><strong>Lineage is recorded, not remembered.</strong> Every dataset carries its sources and transforms, written automatically at run time — tribal knowledge rots, and a bad number with no origin takes days to explain. See the <code class="font-mono text-[13px]">data-lineage</code> skill.</li></ul>""",
        is_open=True,
    ) + "\n"
    + details_card("4 · Shape and keep", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Partition for pruning.</strong> Low-cardinality dates or keys let queries skip whole ranges; high-cardinality IDs spawn thousands of tiny files that slow every reader. Compact on a schedule. See the <code class="font-mono text-[13px]">data-partition</code> skill.</li>
<li><strong>Shapes are built for agent readers.</strong> The old way nested objects for human convenience — deep graphs, clever nulls, tribal abbreviations every new reader had to learn. The new way keeps one canonical flat shape per concept with full-word names and explicit states, because agents re-parse every structure on every read. See the <code class="font-mono text-[13px]">data-model</code> skill.</li>
<li><strong>Expire per policy, prove deletion.</strong> Every dataset gets a written retention rule; PII gets the shortest one, with deletion on request and proof. Keep-forever drowns storage budgets and turns every breach into a GDPR incident. Archive in open formats. See the <code class="font-mono text-[13px]">data-retain</code> skill.</li>
<li><strong>Streams are not batches.</strong> Unbounded transforms need windows plus watermarks so late and out-of-order events settle; every grouping needs an emit trigger, and watermark lag is the health metric. Change data capture streams from the database log — deletes must propagate, which polling can never do (<a href="https://debezium.io/" target="_blank" rel="noopener" class="text-accent underline">Debezium</a> works this way). Merges are keyed, never full overwrites. See the <code class="font-mono text-[13px]">data-streams</code>, <code class="font-mono text-[13px]">data-cdc</code>, and <code class="font-mono text-[13px]">data-upserts</code> skills.</li></ul>""") + "\n"
    + """</section>
"""
)

OPS_BODY = ("""<header class="space-y-2"><h1 class="font-display text-[38px]">Ops guide</h1><p class="text-[17px] max-w-[72ch]">Ship safely, page rarely. Agents operate the system through gated pipelines and measured restores; humans verify the dashboard, the drill record, and the finding counts — never the procedure text.</p></header>
<section class="grid gap-2 my-4">
"""
    + details_card("1 · Gates before prod", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>One shared pipeline, required gates.</strong> Every repo deploys through the same template: build, tests, security scan, approval for production. Hand-rolled pipelines drift until the deploy that matters most is the one least tested. Measure the result the way <a href="https://dora.dev/" target="_blank" rel="noopener" class="text-accent underline">DORA</a> does — speed and stability together: how often you ship, how fast changes land, how often they fail, how fast you recover.</li>
<li><strong>Preview everything, roll out gradually.</strong> Every PR gets an ephemeral production mirror that auto-stops when idle — never production data in previews. Traffic shifts progressively behind health gates with the rollback trigger defined before starting; never 100 percent at once outside an emergency. Deterministic gates around probabilistic actors: agents are probabilistic, gates are deterministic — required checks, fail-closed scans, reversible migrations, and the independent witness. That is the whole architecture: bound the actor, never predict it. See the <code class="font-mono text-[13px]">ops-pipeline</code>, <code class="font-mono text-[13px]">ops-preview</code>, and <code class="font-mono text-[13px]">ops-rollout</code> skills.</li></ul>""",
        is_open=True,
    ) + "\n"
    + details_card("2 · Migrations and secrets", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Expand then contract, always reversible.</strong> Version every schema change and run it with the deploy: add nullable, backfill, constrain, drop — readers never see a half-migrated schema. Dry-run against prod-shaped data; never edit an applied migration. Untested migrations turn deploys into outages with no way back. See the <code class="font-mono text-[13px]">ops-migrate</code> skill.</li>
<li><strong>Inject secrets, rotate automatically.</strong> Vault-backed secrets enter at runtime with RBAC — never committed to repos, never one static value everywhere. Rotation runs on a schedule, not on manual tickets; every read is audited. Manual rotation scatters copies that outlive every fix. See the <code class="font-mono text-[13px]">ops-secrets</code> skill.</li></ul>""") + "\n"
    + details_card("3 · Pages worth waking for", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>One id, symptoms only, runbook attached.</strong> Logs, metrics, and traces unify behind one request id so any alert opens the full story. Alert only on user-facing symptoms — every page actionable with a runbook link, or it becomes noise the team ignores. Dashboards are for debugging, not for watching. See the <code class="font-mono text-[13px]">ops-observe</code> skill.</li>
<li><strong>Signals stay queryable, dashboards stay human.</strong> Health as JSON endpoints and deploy receipts the agent can fetch — queryable signals first, dashboard pixels second; a monitoring <a href="https://modelcontextprotocol.io/" target="_blank" rel="noopener" class="text-accent underline">MCP</a> server beats both. Humans read dashboards; agents read signals. See the <code class="font-mono text-[13px]">ops-observe</code> skill.</li>
<li><strong>Don't trust the system — verify it.</strong> Agents read signals, but one check stays independent: an external probe or status page outside the deploy, plus drill results a human can audit without asking the agent. The monitored system is never the only witness to its own health. See the <code class="font-mono text-[13px]">ops-observe</code> skill.</li>
<li><strong>Blameless reviews, tracked to done.</strong> Page a scheduled rotation with escalation paths — never a single hero with no notes. Postmortems focus on causes, never people (<a href="https://sre.google/sre-book/postmortem-culture/" target="_blank" rel="noopener" class="text-accent underline">Google's SRE book on postmortem culture</a>), and action items stay tracked until done — the review nobody reads is the incident that repeats. See the <code class="font-mono text-[13px]">ops-oncall</code> skill.</li></ul>""",
        is_open=True,
    ) + "\n"
    + details_card("4 · Prove the restore", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>An untested backup is assumed broken.</strong> Back up on a schedule matched to a written RPO — and drill the restore, timed against the RTO, into an isolated environment. A missed RTO changes the strategy, not the apology. See the <code class="font-mono text-[13px]">ops-backup</code> skill.</li>
<li><strong>Reproducible from a clean account.</strong> Every environment version-controlled, drift detection scheduled, state locked and backed up — console click-ops lives in one engineer's head. Processes stay stateless and disposable the <a href="https://12factor.net/" target="_blank" rel="noopener" class="text-accent underline">twelve-factor</a> way so scaling and restarts are boring. Probes split liveness from readiness so broken pods stop getting traffic. See the <code class="font-mono text-[13px]">ops-iac</code>, <code class="font-mono text-[13px]">ops-scale</code>, and <code class="font-mono text-[13px]">ops-probes</code> skills.</li></ul>""") + "\n"
    + details_card("5 · Security operations", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>Every finding owned with a deadline.</strong> Scan continuously and rank by exploitability; block builds on critical images and dependencies, fail closed when the scanner errors. Scan-and-sit is the failure mode — a finding without an owner and a retest sits until it breaches. See the <code class="font-mono text-[13px]">sec-vuln</code> and <code class="font-mono text-[13px]">sec-scan</code> skills.</li>
<li><strong>One IdP, no permanent exceptions.</strong> Enterprise login runs through one provider with phishing-resistant MFA; legacy logins and break-glass accounts expire by date. Sessions stay short-lived with server-side revocation. Secrets in code get revoked first and purged from history. See the <code class="font-mono text-[13px]">sec-sso</code>, <code class="font-mono text-[13px]">sec-session</code>, and <code class="font-mono text-[13px]">sec-secretscan</code> skills.</li>
<li><strong>Detect, contain, prove.</strong> Tamper-evident logs with tested integrity, blocking WAF rules tuned to real traffic, retuned anomaly baselines, drilled containment runbooks, fleet-wide patching, and automated compliance evidence. Hardening the code itself follows the OWASP deep-dives; humans verify finding counts and drill logs. See the <code class="font-mono text-[13px]">sec-index</code> skill and the <a href="/skills" class="text-accent underline">Skills page</a>.</li></ul>""") + "\n"
    + details_card("6 · Agents operate together", """<ul class="text-left space-y-2 list-disc pl-5">
<li><strong>DevOps broke the wall between developers and operators.</strong> One shared pipeline, shared ownership, blameless reviews — so human teams could ship together. It worked, and it has been measured ever since the <a href="https://dora.dev/" target="_blank" rel="noopener" class="text-accent underline">DORA</a> way: speed and stability together.</li>
<li><strong>Agentic ops breaks the same wall between agents.</strong> One shared plan ledger instead of standups, one feature area per agent instead of merge conflicts, idempotent steps instead of careful handoffs, structured status instead of chat threads. When agents share a deploy, they coordinate through the <code class="font-mono text-[13px]">ops-coordinate</code> skill — humans verify the plan ledger and the deploy receipt, never the chat log.</li>
<li><strong>Claims are leases, not intentions.</strong> A task claim goes through the lease endpoint with an agent name and a TTL — a live lease rejects the second claimant, expired leases release on their own. Honor the 409; never work a held task. See the <code class="font-mono text-[13px]">ops-coordinate</code> skill.</li></ul>""") + "\n"
    + """</section>
"""
)


BY_ID = {s.id: s for s in SKILLS}

GROUPS = [
    ("Start here", ["code-index", "ui-index", "code-plan"]),
    ("Always on", ["code-secure", "code-reuse", "code-token"]),
    ("Build services", ["code-language", "ui-mobile", "code-shape", "code-boundaries", "code-polyglot", "code-group", "code-legacy", "code-lifecycle"]),
    ("Build interfaces", ["ui-shell", "ui-tokens", "ui-behavior", "ui-framework", "ui-widgets", "ui-platform-picks", "ui-charts", "ui-chart-twin", "ui-nav", "ui-images", "ui-forms", "ui-a11y"]),
    ("Product features", ["app-index", "code-billing", "code-rbac", "code-invites", "code-notify", "code-search", "code-uploads", "code-auditlog", "code-webhooks", "code-apikeys", "code-flags", "code-impexp"]),
    ("Move data", ["data-index", "data-collect", "data-ingest", "data-orchestrate", "data-etl", "data-contracts", "data-model", "data-backfill", "data-cdc", "data-quality", "data-partition", "data-retain", "data-streams", "data-lineage", "data-upserts", "data-concurrency", "data-metrics", "data-pii"]),
    ("Ship safely", ["ops-index", "ops-pipeline", "ops-release", "ops-observe", "ops-preview", "ops-migrate", "ops-rollout", "ops-secrets", "ops-backup", "ops-iac", "ops-scale", "ops-probes", "ops-oncall", "ops-coordinate", "ops-safety", "sec-index", "sec-vuln", "sec-sso", "sec-scan", "sec-secretscan", "sec-session", "sec-siem", "sec-waf", "sec-anomaly", "sec-runbooks", "sec-patch", "sec-compliance"]),
    ("Security deep-dives", ["code-auth", "code-crypto", "code-injection", "code-design", "code-misconfig", "code-deps", "code-integrity", "code-logging", "code-ssrf", "code-ratelimit"]),
    ("Verify", ["verify-tests", "verify-visual", "verify-layout", "verify-benchmark", "verify-debug"]),
    ("Run well", ["code-cache", "code-track", "code-perf", "code-async", "code-fallback"]),
    ("Get found", ["ui-seo"]),
]

BOARD_SECTIONS = "".join(
    '<section class="mt-6"><h2 class="font-display text-[22px] text-left mb-3">' + title
    + f' <span class="font-mono text-xs text-muted">{len(ids)} skills</span></h2></section>'
    for title, ids in GROUPS
)

BOARD_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">Skills</h1><p>One hundred four skills is far more than any one task needs — and that's the point. Nobody reads them all. Each skill does exactly one job and carries a why, a measured token badge, and verify checks. They are written for our philosophy — code for agents to read, interfaces for humans to judge — not for human maintainers.</p>
<p>How it works: <strong>1.</strong> the bank map routes your task to an area; <strong>2.</strong> your agent fetches only the matched skills with its key; <strong>3.</strong> install only what matches and work from local copies. Small skills plus one map keep every session's context small by design — this is progressive disclosure, and the whole bank is about 23.0k tokens against a typical task pack of 2.4k. Humans judge two things: tests pass, and it looks right.</p>
<div class="bg-ink text-white rounded-xl p-5 text-left"><p class="m-0 font-display text-[22px] mb-3">Get the bank</p><p class="m-0 text-sm">One $9.99 payment, yours forever — up to 10 projects, free updates, no subscription. Your key unlocks the agentic install pack your agent fetches and installs itself.</p><p class="m-0 mt-3"><a href="/#agent" class="inline-block bg-accent text-white rounded-full min-h-[44px] px-5 py-2 no-underline">Get the skills — $9.99 once</a></p></div></header>
""" + BOARD_SECTIONS

MISSING_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">Nothing here.</h1><p><a href="/" class="text-accent underline">Back home</a> · <a href="/skills" class="text-accent underline">Skills</a></p></header>"""

ABOUT_BODY = """<header class="space-y-2"><h1 class="font-display text-[38px]">About me</h1>
<p>Hi, I'm Thao. I live in Southeast Asia and I build things for the web.</p></header>
<section class="mt-4 bg-white border border-solid border-line rounded-xl p-5 space-y-3">
<p class="m-0">I started ai (&#24859;) means love for one simple reason: the old way of writing code was for humans to read. Now agents write most of the code, so code should be easy for agents to read instead. Humans only need to judge two things — do the tests pass, and does it look right.</p>
<p class="m-0">Everything here is free and open. If a skill saves your agent tokens, use it. If something breaks or you have an idea, reach me through the <a href="/#contact" data-open-contact class="text-accent underline">contact us</a> button — I read every message.</p>
<p class="m-0">The code lives on <a href="https://github.com/knivesthao/aimeanslove" target="_blank" rel="noopener" class="text-accent underline">GitHub</a>.</p>
</section>"""


def llms() -> str:
    lines = [
        "# ai (愛) means love",
        "Manifesto: machine builds for machines; humans verify via tests + visual check.",
        "",
        "## Pages",
        "- / ......... manifesto (human summary)",
        "- /ui ....... UI styling + behavior guide",
        "- /code ..... coding guide (Python first, guardrail frameworks)",
        "- /data ..... data pipeline guide (land once, trust but verify)",
        "- /ops ...... ops + security guide (gated deploys, paging, drills)",
        "- /skills ... skill library (all skills, copyable, trimmable install packs)",
        "- /about .... who runs this and why",
        "",
        "## Machine endpoints (skill JSON needs ?key= — one $9.99 key, forever; fields + stats stay open)",
        "- GET /api/skills?key=YOUR_KEY[&track=ui|code|verify&fields=id,prompt,checks]",
        "- GET /api/skill/:id?key=YOUR_KEY[&fields=prompt,checks] (ETag: send If-None-Match → 304)",
        "- GET /api/install?key=YOUR_KEY (full pack + copy-paste install prompt, idempotent via .agents/ailv.json)",
        "- GET /api/fields + /api/stats (open: field names, usage counts)",
        "- GET /board.json?key=YOUR_KEY (full bank, keyed)",
    ]
    lines += [f"- skill {s.id} [{s.track}] {s.tokens}: {s.title}" for s in SKILLS]
    return "\n".join(lines)


app = FastAPI(title="ai (愛) means love")


@app.middleware("http")
async def no_store(request: Request, call_next):
    resp = await call_next(request)
    resp.headers["Cache-Control"] = "no-store"
    return resp


RATE_LIMIT = int(os.environ.get("RATE_LIMIT_PER_MINUTE", "120"))
RATE_BUCKETS: dict[str, deque] = {}


@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path.startswith("/api/"):
        now = time.monotonic()
        ip = request.client.host if request.client else "unknown"
        bucket = RATE_BUCKETS.setdefault(ip, deque())
        while bucket and now - bucket[0] > 60:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT:
            retry = int(60 - (now - bucket[0])) + 1
            return JSONResponse(
                {"ok": False, "error": "too many requests"},
                status_code=429,
                headers={"Retry-After": str(retry)},
            )
        bucket.append(now)
    return await call_next(request)


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


@app.get("/data", response_class=HTMLResponse)
def data_guide() -> str:
    hit("/data")
    return page("Data guide", "Land every event once, move in order, trust but verify.", "/data", DATA_BODY)


@app.get("/ops", response_class=HTMLResponse)
def ops_guide() -> str:
    hit("/ops")
    return page("Ops guide", "Gated deploys, paging that matters, drilled restores.", "/ops", OPS_BODY)


@app.get("/about", response_class=HTMLResponse)
def about() -> str:
    hit("/about")
    return page("About me", "Who runs ai (愛) means love and why it exists.", "/about", ABOUT_BODY)


def releases_section() -> str:
    items = "".join(
        f"<li><strong>{v} — {d} — {title}.</strong> {notes}</li>" for v, d, title, notes in RELEASES
    )
    return (
        '<section class="mt-10 border-t-2 border-solid border-ink pt-5 space-y-3">'
        '<h2 class="font-display text-[22px] mb-3">Releases</h2>'
        '<p class="text-sm max-w-[72ch]">The bank grows in public. Every change ships with notes and a feed — subscribe once, read the diff, update on your schedule. Nothing here changes silently under a pinned install.</p>'
        f'<ul class="text-left space-y-2 list-disc pl-5">{items}</ul></section>'
    )


@app.get("/skills", response_class=HTMLResponse)
def skills_page() -> str:
    hit("/skills")
    return page("Skills", "Read the index, install only the matched skills, skip the rest.", "/skills", BOARD_BODY + releases_section())


@app.get("/board", response_class=HTMLResponse)
def board() -> Response:
    return RedirectResponse("/skills", status_code=302)


CONTACT_TO = os.environ.get("CONTACT_TO", "knives.thao@gmail.com")


def contact_dialog(errors=(), values=None, force_open=False) -> str:
    """Contact dialog. Errors render inline (summary + per-field), values preserved."""
    values = values or {}
    bad = {f for f, _ in errors}
    first_bad = next((f for f, _ in errors), "")
    err_list = "".join(f"<li>{html.escape(m)}</li>" for _, m in errors)
    err_block = (
        '<div role="alert" class="bg-wash border border-solid border-line rounded-lg p-2.5 text-sm text-left">'
        "<p class='m-0'><strong>Please fix:</strong></p>"
        f"<ul class='text-left space-y-1 pl-5 list-disc'>{err_list}</ul></div>"
        if errors else ""
    )
    def field(kind, fid, name, label, extra=""):
        v = html.escape(values.get(name, ""), quote=True)
        inv = ' aria-invalid="true"' if name in bad else ""
        foc = " autofocus" if name == first_bad else ""
        if kind == "area":
            control = f'<textarea id="{fid}" name="{name}" required maxlength="5000" rows="5"{inv}{foc} class="w-full border border-solid border-line rounded-lg px-3 py-2 bg-white">{v}</textarea>'
        else:
            control = f'<input id="{fid}" name="{name}" type="{kind}" required maxlength="200" autocomplete="{extra}" value="{v}"{inv}{foc} class="w-full border border-solid border-line rounded-lg px-3 py-2 bg-white">'
        return (f'<p class="m-0"><label class="block text-sm mb-1" for="{fid}">{label}</label>'
                f"{control}</p>")
    open_attr = " open" if force_open else ""
    opener = "<script>document.getElementById('contact-dialog')?.showModal()</script>" if force_open else ""
    return (
        f'<dialog id="contact-dialog"{open_attr} class="rounded-xl border border-solid border-line bg-white p-5 text-left text-ink max-w-[420px] backdrop:bg-ink/60">'
        '<p class="font-display text-[22px] mb-3">Contact us</p>'
        "<p class='m-0 text-sm'>Ask a question, report a bug, or just say hi. A human reads every message.</p>"
        + err_block +
        '<form method="post" action="/contact" class="space-y-3 text-left mt-3">'
        + field("text", "cf-name", "name", "Your name", "name")
        + field("email", "cf-email", "email", "Your email", "email")
        + '<p class="m-0" hidden aria-hidden="true"><label>Company<input name="company" tabindex="-1" autocomplete="off"></label></p>'
        + field("area", "cf-message", "message", "Message")
        + '<p class="m-0"><button type="submit" class="cursor-pointer bg-accent text-white rounded-full px-4 py-2 min-h-[44px]">Send message</button></p>'
        "</form>"
        '<div class="mt-3 text-right"><button type="button" data-close-contact class="cursor-pointer border border-solid border-line bg-white rounded-lg px-3 py-1.5 min-h-[44px]">Close</button></div>'
        "</dialog>" + opener
    )


def send_contact_email(name: str, email: str, message: str) -> tuple[bool, str]:
    key = os.environ.get("RESEND_API_KEY", "")
    if not key:
        return False, "missing-key"
    payload = json.dumps({
        "from": "Contact form <onboarding@resend.dev>",
        "to": [CONTACT_TO],
        "reply_to": email,
        "subject": f"aimeanslove contact from {name}",
        "text": f"From: {name} <{email}>\n\n{message}",
    }).encode()
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return (200 <= r.status < 300), ("sent" if 200 <= r.status < 300 else f"http-{r.status}")
    except Exception as e:
        return False, f"error-{type(e).__name__}"


def thanks_page() -> str:
    return page("Thanks", "Message received.", "/contact",
                '<header class="space-y-2"><h1 class="font-display text-[38px]">Thanks</h1>'
                "<p>Your message is on its way. We read everything.</p>"
                '<p><a href="/" class="text-accent underline">Back home</a></p></header>')


def sorry_page(note: str) -> str:
    return page("Sorry", "Message not sent.", "/contact",
                '<header class="space-y-2"><h1 class="font-display text-[38px]">Sorry</h1>'
                "<p>" + html.escape(note) + "</p>"
                '<p><a href="/" class="text-accent underline">Back home</a></p></header>')


@app.post("/contact", response_class=HTMLResponse)
async def contact_post(request: Request):
    hit("/contact")
    form = await request.form()
    name = str(form.get("name", "")).strip()
    email = str(form.get("email", "")).strip()
    message = str(form.get("message", "")).strip()
    if str(form.get("company", "")).strip():
        return thanks_page()
    domain = email.split("@")[-1] if "@" in email else ""
    errors = []
    if not name or len(name) > 100:
        errors.append(("name", "Your name is needed (100 characters or fewer)."))
    if "." not in domain:
        errors.append(("email", "That email address doesn't look right — a valid email address is needed."))
    if not message or len(message) > 5000:
        errors.append(("message", "Your message is needed (5000 characters or fewer)."))
    if errors:
        values = {"name": name, "email": email, "message": message}
        return HTMLResponse(
            page("Contact", "Fix the highlighted fields and resend.", "/contact",
                 '<header class="space-y-2"><h1 class="font-display text-[38px]">Message not sent</h1>'
                 "<p>Fix the highlighted fields below and send again.</p></header>"
                 + contact_dialog(errors, values, force_open=True)),
            status_code=400,
        )
    sent, _reason = send_contact_email(name, email, message)
    if sent:
        return thanks_page()
    return sorry_page("Thanks for writing — but email sending is not set up yet, so your message wasn't sent. Please check back soon.")


@app.get("/api", include_in_schema=False)
@app.get("/keys", include_in_schema=False)
def old_api(request: Request) -> RedirectResponse:
    hit(request.url.path)
    return RedirectResponse("/skills", status_code=302)


@app.get("/llms.txt", response_class=PlainTextResponse)
def llms_txt() -> str:
    hit("/llms.txt")
    return llms()


@app.get("/robots.txt", response_class=PlainTextResponse)
def robots() -> str:
    hit("/robots.txt")
    return "User-agent: *\nAllow: /\nSitemap: https://aimeanslove.fyi/sitemap.xml\n"


SITE_URL = "https://aimeanslove.fyi"
SITEMAP_PAGES = ["/", "/code", "/ui", "/data", "/ops", "/skills", "/about"]


RELEASES = [
    ("v1.0.0", "2026-11-07", "Signed, leased, measured", "102 skills, every one signed. Lease claims, canary comparator, human-first safety, measured proof section."),
    ("2026-11-07", "2026-11-07", "Test hardening + sourced charts", "Lifecycle coverage tests. ui-chart-twin split. Cleveland-McGill, W3C tables, Vega-Lite twin, all backlinked."),
    ("2026-11-07", "2026-11-07", "Agentic ops", "Data + Ops philosophy guides. ops-coordinate, queryable observe, don't-trust-the-system."),
    ("2026-11-07", "2026-11-07", "Async, concurrency, model", "code-async handoff, data-concurrency, data-model."),
    ("2026-11-07", "2026-11-07", "Foundation", "92-skill bank. Guides go philosophy-with-sources. Skills page pitches install-matched."),
]


@app.get("/releases", response_class=HTMLResponse)
def releases_page(request: Request) -> Response:
    hit("/releases")
    return RedirectResponse("/skills", status_code=302)


@app.get("/releases.xml")
def releases_feed() -> Response:
    hit("/releases.xml")
    items = "".join(
        f"<item><title>{v} — {title}</title><link>{SITE_URL}/skills</link>"
        f"<pubDate>Sat, 07 Nov 2026 00:00:00 +0000</pubDate><description>{notes}</description></item>"
        for v, d, title, notes in RELEASES
    )
    body = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<rss version="2.0"><channel><title>ai (&#24859;) means love — releases</title>'
            f"<link>{SITE_URL}/skills</link><description>Skill bank release notes.</description>"
            + items + "</channel></rss>")
    return Response(content=body, media_type="application/rss+xml")


@app.get("/sitemap.xml")
def sitemap() -> Response:
    hit("/sitemap.xml")
    urls = "".join(f"<url><loc>{SITE_URL}{p}</loc></url>" for p in SITEMAP_PAGES)
    body = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>"
    return Response(content=body, media_type="application/xml")


@app.get("/board.json")
def board_json(request: Request) -> Response:
    hit("/board.json")
    digest = _require_key(request)
    if isinstance(digest, Response):
        return digest
    return etagged(request, {"ok": True, "count": len(SKILLS), "skills": [s.model_dump() for s in SKILLS]})


CLAIMS: dict[str, dict] = {}


def prune_claims() -> None:
    now = time.time()
    for task in [t for t, c in CLAIMS.items() if c["expires"] <= now]:
        del CLAIMS[task]


@app.post("/api/plan/claim")
async def plan_claim(request: Request) -> Response:
    form = await request.form()
    task, agent = (form.get("task") or "").strip(), (form.get("agent") or "").strip()
    try:
        ttl = min(max(int(form.get("ttl") or 600), 0), 86400)
    except ValueError:
        return JSONResponse({"ok": False, "error": "ttl must be seconds"}, status_code=400)
    if not task or not agent:
        return JSONResponse({"ok": False, "error": "task and agent required"}, status_code=400)
    prune_claims()
    if task in CLAIMS:
        return JSONResponse({"ok": False, "error": f"held by {CLAIMS[task]['agent']}"}, status_code=409)
    CLAIMS[task] = {"agent": agent, "expires": time.time() + ttl}
    return JSONResponse({"ok": True, "task": task, "agent": agent, "ttl": ttl})


@app.post("/api/plan/release")
async def plan_release(request: Request) -> Response:
    form = await request.form()
    task, agent = (form.get("task") or "").strip(), (form.get("agent") or "").strip()
    prune_claims()
    if task not in CLAIMS:
        return JSONResponse({"ok": False, "error": "no such claim"}, status_code=404)
    if CLAIMS[task]["agent"] != agent:
        return JSONResponse({"ok": False, "error": f"held by {CLAIMS[task]['agent']}"}, status_code=403)
    del CLAIMS[task]
    return JSONResponse({"ok": True, "task": task})


@app.get("/api/plan/claims")
def plan_claims() -> Response:
    prune_claims()
    return JSONResponse({"ok": True, "claims": [{"task": t, **c} for t, c in CLAIMS.items()]})


@app.get("/brand/{name}")
def brand_asset(name: str) -> Response:
    allowed = {
        "og-card.png": "image/png", "favicon.png": "image/png",
        "hero-mark.jpg": "image/jpeg",
    }
    if name not in allowed:
        return JSONResponse({"ok": False, "error": "no such asset"}, status_code=404)
    return Response(content=(ROOT / "public" / "brand" / name).read_bytes(), media_type=allowed[name])


@app.get("/signatures.json")
def signatures_json(request: Request) -> Response:
    hit("/signatures.json")
    try:
        return etagged(request, json.loads((ROOT / "signatures.json").read_text(encoding="utf-8")))
    except OSError:
        return JSONResponse({"ok": False, "error": "bank not signed yet"}, status_code=503)


@app.get("/api/install")
def api_install(request: Request) -> Response:
    hit("/api/install")
    digest = _require_key(request)
    if isinstance(digest, Response):
        return digest
    pack = [
        {
            "id": s.id,
            "file": f".agents/skills/{s.id}/SKILL.md",
            "content": (
                f"---\nname: {s.id}\ndescription: {s.why}\n---\n\n"
                f"# {s.title}\n\n{s.prompt}\n\n## Checks\n\n"
                + "\n".join("- " + c for c in s.checks) + "\n"
            ),
        }
        for s in SKILLS
    ]
    return etagged(request, {
        "ok": True,
        "count": len(pack),
        "version": BANK_VERSION,
        "marker": ".agents/ailv.json",
        "howto": "Write each item to its file path, then work from local copies and never refetch mid-task.",
        "prompt": INSTALL_PROMPT.format(count=len(pack), version=BANK_VERSION, pack="the install array in this response"),
        "install": pack,
    })


@app.post("/api/install/receipt")
async def install_receipt(request: Request) -> Response:
    hit("/api/install/receipt")
    digest = _require_key(request)
    if isinstance(digest, Response):
        return digest
    try:
        body = await request.json()
    except ValueError:
        return JSONResponse({"ok": False, "error": "send JSON: {version, install_id, installed[], kept[]}"}, status_code=400)
    if not isinstance(body, dict) or not isinstance(body.get("installed"), list) or not isinstance(body.get("kept"), list):
        return JSONResponse({"ok": False, "error": "send JSON: {version, install_id, installed[], kept[]}"}, status_code=400)
    iid = str(body.get("install_id") or "").strip()
    if not iid or len(iid) > 128:
        return JSONResponse({"ok": False, "error": "install_id required (uuid per project, reused on updates)"}, status_code=400)
    version = str(body.get("version") or "unknown")
    if not _record_install(digest, iid, version):
        return JSONResponse({"ok": False, "error": "install limit reached for this key — updates on existing installs still work; contact us for a team key"}, status_code=429)
    STATS["install_receipts"] += 1
    STATS["install_versions"][version] = STATS["install_versions"].get(version, 0) + 1
    try:
        STATS_FILE.write_text(json.dumps(STATS), encoding="utf-8")
    except OSError:
        pass
    return JSONResponse({"ok": True, "receipts": STATS["install_receipts"]})


@app.get("/api/skills")
def api_skills(request: Request, track: str | None = Query(default=None), fields: str | None = None) -> Response:
    hit("/api/skills")
    digest = _require_key(request)
    if isinstance(digest, Response):
        return digest
    bank = [s for s in SKILLS if s.track == track] if track else list(SKILLS)
    return etagged(request, {"ok": True, "count": len(bank), "skills": [pick_fields(s, fields) for s in bank]})


@app.get("/api/skill/{sid}")
def api_skill(request: Request, sid: str) -> Response:
    hit("/api/skill/:id", sid)
    digest = _require_key(request)
    if isinstance(digest, Response):
        return digest
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
    return etagged(request, {"ok": True, "version": BANK_VERSION, "stats": STATS})


@app.post("/api/copy")
def api_copy(request: Request) -> Response:
    hit("/api/copy")
    sid = request.query_params.get("skill", "")
    if sid not in BY_ID:
        return JSONResponse({"ok": False, "error": "unknown skill"}, status_code=404)
    STATS["pending_copies"] += 1
    try:
        STATS_FILE.write_text(json.dumps(STATS), encoding="utf-8")
    except OSError:
        pass
    return Response(status_code=204)


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
