"""Open endpoints + usage tracking. Run: .venv/bin/python test/api_test.py"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
PORT = os.environ.get("TEST_PORT", "8797")
USAGE_FILE = "/tmp/mf-test-usage.json"
try:
    os.unlink(USAGE_FILE)
except OSError:
    pass


def get(path, headers=None):
    req = urllib.request.Request(f"http://localhost:{PORT}{path}", headers=headers or {})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def post(path, data):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(f"http://localhost:{PORT}{path}", data=body)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


child = subprocess.Popen(
    [sys.executable, "server.py"],
    cwd=ROOT,
    env={**os.environ, "PORT": PORT, "USAGE_FILE": USAGE_FILE, "RESEND_API_KEY": ""},
    stdout=subprocess.DEVNULL,
)
try:
    time.sleep(2.5)
    status, _, _ = get("/api/skills")
    assert status == 200, f"skills open without key, got {status}"

    status, _, _ = get("/api/skill/nope")
    assert status == 404, f"unknown skill 404s, got {status}"

    status, headers, _ = get("/api/skill/code-secure?fields=prompt")
    assert status == 200
    tag = next((v for k, v in headers.items() if k.lower() == "etag"), None)
    assert tag, "etag present"
    status, _, body = get("/api/skill/code-secure?fields=prompt", {"If-None-Match": tag})
    assert status == 304, f"repeat returns 304, got {status}"
    assert body == b"", "304 has empty body"

    # /api redirects to /board (no auto-redirect via low-level call)
    import http.client

    conn = http.client.HTTPConnection("localhost", int(PORT))
    conn.request("GET", "/api")
    r = conn.getresponse()
    assert r.status == 302, f"/api redirects, got {r.status}"
    assert r.getheader("Location").endswith("/board")
    conn.close()

    status, _, body = get("/api/stats")
    stats = json.loads(body)["stats"]
    assert stats["requests"] >= 6, f"requests={stats['requests']}"
    assert stats["skills"].get("code-secure", 0) >= 2, "skill hits counted"
    assert stats["skills"].get("nope", 0) >= 1, "unknown skill counted"
    assert stats["routes"]["/api/skill/:id"] == stats["skills"].get("code-secure", 0) + stats["skills"].get("nope", 0)
    assert os.path.exists(USAGE_FILE), "counts persisted"
    status, _, body = get("/api/skills?fields=id,why")
    bank = json.loads(body)["skills"]
    assert len(bank) == 30 and all(s.get("why") for s in bank), "every skill explains why"
    status, _, body = get("/api/skills?fields=id,prompt")
    for s in json.loads(body)["skills"]:
        local = ROOT / ".agents" / "skills" / s["id"] / "SKILL.md"
        assert local.exists(), f"bank skill {s['id']} installed locally"
        assert s["prompt"] in local.read_text(encoding="utf-8"), f"local {s['id']} matches bank"
    status, _, body = get("/api/skill/code-index?fields=prompt")
    index_map = json.loads(body)["skill"]["prompt"]
    assert all(s["id"] in index_map for s in bank if s["id"] != "code-index"), "index maps every skill"
    assert "house rule beats the skill" in index_map, "stack skills defer to existing codebases"
    status, _, body = get("/")
    assert status == 200 and 'id="menubtn"' in body.decode(), "mobile hamburger present"
    status, _, _ = get("/skills.json")
    assert status == 404, "slim index endpoint is gone; board.json is the one JSON"
    status, _, body = get("/api/skills?fields=id,prompt")
    for s in json.loads(body)["skills"]:
        assert s["prompt"].startswith("Create and install a skill named"), s["id"]
    status, _, body = get("/api/skill/ui-shell?fields=prompt,checks")
    shell = json.loads(body)["skill"]
    assert "aria-label" in shell["prompt"] and "icon-only" in shell["prompt"], "ui-shell allows human UI + metadata"
    assert "360px" in shell["prompt"] and "360px" in shell["checks"][0], "ui-shell is mobile-first"
    assert "Lucide" in shell["prompt"], "ui-shell names Lucide, no hand SVG"
    assert any("aria-label" in c for c in shell["checks"]), "metadata check present"
    assert any("data-action" in c for c in shell["checks"]), "data-action check present"
    status, _, body = get("/api/skill/verify-visual?fields=prompt")
    visual = json.loads(body)["skill"]
    assert "shots/" in visual["prompt"], "verify-visual saves screenshots to shots/"
    assert "headless" in visual["prompt"], "verify-visual never trusts headless shots alone"

    status, _, body = get("/board")
    assert status == 200, f"board renders, got {status}"
    html = body.decode()
    assert "code-reuse" in html and "Reuse before you build" in html, "board lists skills"
    assert "code-index" in html and "progressive disclosure" in html, "index skill maps tasks to skills"
    assert "code-ssrf" in html and "code-crypto" in html, "OWASP set renders on board"
    assert all(g in html for g in ("Start here", "Always on", "Security deep-dives", "Verify", "Run well")), "board groups skills"
    assert html.count("data-copy-skill=") == 30, "every skill renders exactly once"
    assert "data-copy-skill" in html, "board has copy buttons"
    assert 'id="q"' not in html and "data-track" not in html, "no filter machinery"
    assert 'href="/about"' in html, "about linked from header and footer"
    assert "min-h-screen" in html and "flex-1" in html, "flex shell pins footer to the bottom"
    assert "max-w-[62ch] mx-auto" not in html, "content left-aligns, no centered blocks"
    assert "62ch" not in html, "every block spans the same content width"
    assert "humans verify" not in html, "old footer tagline is gone"
    status, _, body = get("/about")
    assert status == 200 and "About me" in body.decode(), "about page renders"
    assert "github.com/knivesthao/aimeanslove" in body.decode(), "about links the repo"
    assert 'id="contact-dialog"' in html and "data-open-contact" in html, "contact lives in a dialog, not a page"
    assert 'name="company"' in html, "contact dialog has honeypot"
    status, _, _ = get("/contact")
    assert status == 405, "GET /contact is POST-only, no page to render"
    status, _, body = post("/contact", {"name": "A", "email": "not-an-email", "message": "hi"})
    assert status == 400 and "valid email" in body.decode(), "bad email rejected with guidance"
    status, _, body = post("/contact", {"name": "A", "email": "a@b.co", "message": "hi", "company": "bot"})
    assert status == 200 and "on its way" in body.decode(), "honeypot gets silent thanks"
    status, _, body = post("/contact", {"name": "A Tester", "email": "a@b.co", "message": "hello"})
    assert status == 200 and "not set up yet" in body.decode(), "missing key fails gracefully, no crash"
    visible = re.sub(r"<script.*?</script>", "", html, flags=re.S)
    assert "/llms.txt" not in visible and "/api/stats" not in visible, "no machine links on human pages"
    status, _, _ = get("/", {"User-Agent": "Mozilla/5.0 (compatible; GPTBot/1.1)"})
    assert status == 200, "crawlers can fetch pages"
    status, _, body = get("/robots.txt")
    assert status == 200 and "Allow: /" in body.decode(), "robots.txt welcomes crawlers"
    status, _, body = get("/api/stats")
    routes_before = json.loads(body)["stats"]["routes"]
    fetched_before = sum(routes_before.get(k, 0) for k in ("/board.json", "/api/skills", "/api/skill/:id"))
    status, _, _ = get("/board")
    assert status == 200, "page views still render"
    status, _, _ = get("/board.json")
    status, _, _ = get("/api/skills?track=code")
    status, _, _ = get("/api/skill/code-language?fields=id")
    status, _, body = get("/board")
    html = body.decode()
    m = re.search(r'href="/#agent"[^>]*>\s*(\d+)', html)
    assert m, "board shows usage counter badge"
    assert int(m.group(1)) == fetched_before + 3, f"counter counts skill fetches only, got {m.group(0)} after {fetched_before}"
    badge_before = int(m.group(1))
    status, _, _ = post("/api/copy?skill=code-secure", {})
    assert status == 204, f"copy beacon accepted, got {status}"
    status, _, _ = post("/api/copy?skill=code-index", {})
    assert status == 204
    status, _, _ = post("/api/copy?skill=nope", {})
    assert status == 404, "unknown skill copy rejected"
    status, _, body = get("/board")
    m = re.search(r'href="/#agent"[^>]*>\s*(\d+)', body.decode())
    assert m and int(m.group(1)) == badge_before, "copies sit pending, badge waits for rollup"
    status, _, body = get("/api/stats")
    stats = json.loads(body)["stats"]
    assert stats["pending_copies"] == 2 and stats["copies_applied"] == 0, "copies bucketed, nothing applied yet"
    sys.path.insert(0, str(ROOT))
    import server as srv
    srv.STATS_FILE = Path("/tmp/mf-test-rollup.json")
    srv.STATS["pending_copies"] = 2
    srv.STATS["copies_applied"] = 0
    srv.STATS["last_rollup"] = "2000-01-01T00:00:00+00:00"
    srv.rollup_copies()
    assert srv.STATS["pending_copies"] == 0 and srv.STATS["copies_applied"] == 2, "rollup absorbs pending copies"
    assert srv.STATS["last_rollup"] > "2000-01-01", "rollup stamps its time"
    assert ">Manifesto</a>" not in html, "manifesto link removed from nav"
    assert 'href="/"' in html, "brand links home"
    assert "data-open-support" in html and "support us" in html, "support button opens dialog"
    assert 'data-dropdown-toggle="mobile-menu"' in html, "menu opens via Flowbite dropdown"
    assert "flowbite@2.5.2" in html, "Flowbite pinned"
    status, _, body = get("/")
    home = body.decode()
    assert status == 200 and 'id="support-dialog"' in home, "dialog on every page"
    status, _, body = get("/ui")
    assert status == 200 and "Flowbite" in body.decode(), "guide names Flowbite for components"
    status, _, body = get("/code")
    assert status == 200 and "Framework first" in body.decode(), "guide states framework-first rule"
    assert 'target="_blank" rel="noopener"' in body.decode(), "external links open a new tab"
    status, _, body = get("/api/skill/ui-framework?fields=prompt")
    lit = json.loads(body)["skill"]
    assert "Flowbite" in lit["prompt"] and "React" in lit["prompt"], "ui-framework keeps Flowbite pieces, rules out heavy frameworks"
    assert "WebAwesome" in lit["prompt"], "ui-framework names WebAwesome for island pieces"
    status, _, body = get("/board")
    board = body.decode()
    assert "<uses-badge" in board, "usage badge is a Lit island"
    assert "lit@3.3.3" in board and 'type="module"' in board, "Lit island pinned and wired"
    assert 'data-lucide="download"' in home, "badge uses Lucide icon"
    assert "createIcons" in home and "lucide@1.69.0" in home, "Lucide pinned and initialized"
    limited = 0
    retry_after = False
    for _ in range(150):
        status, headers, _ = get("/api/fields")
        if status == 429:
            limited += 1
            retry_after = retry_after or any(k.lower() == "retry-after" for k in headers)
    assert limited >= 1, "hammering the API trips the limiter"
    assert retry_after, "429 carries Retry-After"
    print("PASS: open endpoints + usage stats + board")
finally:
    child.terminate()
