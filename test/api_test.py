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
KEYS_FILE = "/tmp/mf-test-keys.json"
TEST_KEY = "ailv_test_" + "x" * 32
TEST_KEY_SOLO = "ailv_test_" + "y" * 32
import hashlib as _hl

with open(KEYS_FILE, "w", encoding="utf-8") as _kf:
    json.dump({"keys": {
        _hl.sha256(TEST_KEY.encode()).hexdigest(): {"label": "test", "active": True, "uses": 0},
        _hl.sha256(TEST_KEY_SOLO.encode()).hexdigest(): {"label": "solo", "active": True, "uses": 0, "cap": 1},
    }}, _kf)
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


def kget(path, headers=None):
    sep = "&" if "?" in path else "?"
    return get(f"{path}{sep}key={TEST_KEY}", headers)


def jpost(path, obj, headers=None):
    raw = json.dumps(obj).encode()
    req = urllib.request.Request(f"http://localhost:{PORT}{path}", data=raw, headers={"Content-Type": "application/json", **(headers or {})})
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
    env={**os.environ, "PORT": PORT, "USAGE_FILE": USAGE_FILE, "AILV_KEYS_FILE": KEYS_FILE, "RESEND_API_KEY": ""},
    stdout=subprocess.DEVNULL,
)
try:
    time.sleep(2.5)
    status, _, body = get("/api/skills")
    assert status == 403, f"skills locked without key, got {status}"
    status, _, _ = get("/api/skills?key=nope")
    assert status == 403, f"skills locked with bad key, got {status}"
    status, _, body = kget("/api/skills?fields=id")
    assert status == 200 and len(json.loads(body)["skills"]) == 102, "valid key reads the bank"
    status, _, _ = get("/board.json")
    assert status == 403, f"board locked without key, got {status}"

    status, _, _ = get("/api/skill/nope")
    assert status == 403, f"skill locked without key, got {status}"
    status, _, _ = kget("/api/skill/nope")
    assert status == 404, f"unknown skill 404s with key, got {status}"

    status, _, body = get("/api/install")
    assert status == 403, f"install without key refused, got {status}"
    status, _, body = get("/api/install?key=nope")
    assert status == 403 and b"invalid or revoked" in body, "bad key refused"
    status, _, body = get(f"/api/install?key={TEST_KEY}")
    assert status == 200, f"valid key installs, got {status}"
    pack = json.loads(body)
    assert pack["count"] == 102 and len(pack["install"]) == 102, "install pack covers the bank"
    first = pack["install"][0]
    assert first["file"].endswith("/SKILL.md") and first["content"].startswith("---"), "install items are writable skill files"
    assert pack["version"] == "1.0.0" and pack["marker"] == ".agents/ailv.json", "install pins version + marker"
    assert ".agents/ailv.json" in pack["prompt"] and "unification, never duplication" in pack["prompt"], "install prompt reviews existing skills first"
    assert "never refetch mid-task" in pack["prompt"], "install prompt works from local copies"
    assert "/api/stats" in pack["prompt"], "install prompt checks version before fetching"
    assert "install/receipt" in pack["prompt"], "install prompt reports success back"
    status, _, _ = jpost("/api/install/receipt", {"version": "1.0.0", "installed": ["code-index"], "kept": []})
    assert status == 403, f"receipt locked without key, got {status}"
    status, _, _ = jpost(f"/api/install/receipt?key={TEST_KEY}", {"nope": True})
    assert status == 400, f"receipt rejects bad body, got {status}"
    status, _, body = jpost(f"/api/install/receipt?key={TEST_KEY}", {"version": "1.0.0", "install_id": "t1", "installed": ["code-index"], "kept": []})
    receipt = json.loads(body)
    assert status == 200 and receipt["ok"] and receipt["receipts"] == 1, "valid receipt tracked"
    status, _, body = kget("/api/stats")
    stats = json.loads(body)["stats"]
    assert stats["install_receipts"] == 1 and stats["install_versions"].get("1.0.0") == 1, "receipts visible in stats"
    for i in range(9):
        status, _, _ = jpost(f"/api/install/receipt?key={TEST_KEY}", {"version": "1.0.0", "install_id": f"cap{i}", "installed": [], "kept": []})
        assert status == 200, f"seat {i} installs, got {status}"
    status, _, body = jpost(f"/api/install/receipt?key={TEST_KEY}", {"version": "1.0.0", "install_id": "capX", "installed": [], "kept": []})
    assert status == 429 and b"install limit" in body, "eleventh seat refused, updates untouched"
    status, _, body = jpost(f"/api/install/receipt?key={TEST_KEY}", {"version": "2.0.0", "install_id": "t1", "installed": [], "kept": []})
    assert status == 200, "updates on known installs never blocked"
    status, _, _ = jpost(f"/api/install/receipt?key={TEST_KEY_SOLO}", {"version": "1.0.0", "install_id": "solo-1", "installed": [], "kept": []})
    assert status == 200, "cap-1 key installs once"
    status, _, _ = jpost(f"/api/install/receipt?key={TEST_KEY_SOLO}", {"version": "1.0.0", "install_id": "solo-2", "installed": [], "kept": []})
    assert status == 429, "per-key cap override honored"

    status, headers, _ = kget("/api/skill/code-secure?fields=prompt")
    assert status == 200
    tag = next((v for k, v in headers.items() if k.lower() == "etag"), None)
    assert tag, "etag present"
    status, _, body = kget("/api/skill/code-secure?fields=prompt", {"If-None-Match": tag})
    assert status == 304, f"repeat returns 304, got {status}"
    assert body == b"", "304 has empty body"

    # /api redirects to /skills (no auto-redirect via low-level call)
    import http.client

    conn = http.client.HTTPConnection("localhost", int(PORT))
    conn.request("GET", "/api")
    r = conn.getresponse()
    assert r.status == 302, f"/api redirects, got {r.status}"
    assert r.getheader("Location").endswith("/skills")
    conn.close()

    status, _, body = get("/api/stats")
    stats = json.loads(body)["stats"]
    assert stats["requests"] >= 6, f"requests={stats['requests']}"
    assert stats["skills"].get("code-secure", 0) >= 2, "skill hits counted"
    assert stats["skills"].get("nope", 0) >= 1, "unknown skill counted"
    assert stats["routes"]["/api/skill/:id"] == stats["skills"].get("code-secure", 0) + stats["skills"].get("nope", 0)
    assert os.path.exists(USAGE_FILE), "counts persisted"
    status, _, body = kget("/api/skills?fields=id,why")
    bank = json.loads(body)["skills"]
    assert len(bank) == 102 and all(s.get("why") for s in bank), "every skill explains why"
    status, _, body = kget("/api/skills?fields=id,prompt")
    for s in json.loads(body)["skills"]:
        local = ROOT / ".agents" / "skills" / s["id"] / "SKILL.md"
        assert local.exists(), f"bank skill {s['id']} installed locally"
        assert s["prompt"] in local.read_text(encoding="utf-8"), f"local {s['id']} matches bank"
    status, _, body = kget("/api/skill/code-index?fields=prompt")
    index_map = json.loads(body)["skill"]["prompt"]
    status, _, body = kget("/api/skill/ui-index?fields=prompt")
    ui_map = json.loads(body)["skill"]["prompt"]
    status, _, body = kget("/api/skill/ui-widgets?fields=prompt")
    widgets_map = json.loads(body)["skill"]["prompt"]
    area_maps = {}
    for area in ("app-index", "data-index", "ops-index", "sec-index"):
        status, _, body = kget(f"/api/skill/{area}?fields=prompt")
        area_maps[area] = json.loads(body)["skill"]["prompt"]
    assert "ui-index" in index_map, "bank index points at the area index"
    assert "ui-widgets" in ui_map and "ui-platform-picks" in ui_map, "area index points at widgets and picks"
    assert all(a in index_map for a in area_maps), "bank index points at the four area indexes"
    assert all(
        s["id"] in index_map or s["id"] in ui_map or s["id"] in widgets_map or any(s["id"] in m for m in area_maps.values())
        for s in bank if s["id"] not in ("code-index", "ui-index", "ui-widgets", "app-index", "data-index", "ops-index", "sec-index")
    ), "every skill reachable by walking the index tree"
    assert "house rule beats the skill" in index_map, "stack skills defer to existing codebases"
    assert "regulated data" in index_map, "bank index routes regulated data to sec-index"
    status, _, body = kget("/api/skill/sec-compliance?fields=prompt")
    compliance = json.loads(body)["skill"]["prompt"]
    assert "HIPAA" in compliance and "code-auditlog" in compliance, "compliance names HIPAA and routes to the audit trail"
    status, _, body = kget("/api/skill/code-auditlog?fields=prompt")
    assert "whether or not HIPAA applies" in json.loads(body)["skill"]["prompt"], "audit trail states its non-HIPAA trigger"
    assert "OWASP" in index_map, "bank index names the OWASP set"
    assert "OWASP" in area_maps["sec-index"], "sec index points at OWASP deep-dives"
    status, _, body = kget("/api/skill/sec-waf?fields=prompt")
    assert "code-injection" in json.loads(body)["skill"]["prompt"], "WAF rules reference injection payloads"
    status, _, body = kget("/api/skill/code-plan?fields=prompt")
    plan = json.loads(body)["skill"]["prompt"]
    assert "inline if five steps or fewer" in plan, "short plans stay inline"
    assert "execute all unblocked steps together" in plan, "independents run in parallel"
    assert "in one batched request" in plan and "execution fetches nothing" in plan, "skills fetched once up front"
    assert "Three or more" in plan, "plan states its explicit skill-count trigger"
    assert "last step is always cleanup" in plan, "plan ends with scratch cleanup"
    assert "maps don't count" in plan, "plan excludes maps and always-on from the count"
    assert "only matched leaves count" in plan, "plan states crossing maps is free"
    assert "Three or more matched skills → code-plan first" in index_map, "bank index routes by skill count"
    assert "Work that outlives the request" in index_map, "bank index routes async handoff"
    assert "parallel fan-out" in index_map, "bank index matches literal parallel triggers"
    status, _, body = kget("/api/skill/code-perf?fields=prompt")
    assert "code-async" in json.loads(body)["skill"]["prompt"], "perf hands off to async by name"
    assert "in one batched request" in index_map and "never fetch the same skill twice" in index_map, "bank index states fetch-once protocol"
    assert "mixed tasks match more than one line" in index_map, "bank index splits mixed UI-plus-API tasks"
    assert "Step zero" in index_map, "bank index detects the stack before matching"
    assert "verify-layout for layout" in index_map, "bank index routes layout proof"
    assert "Two or more agents sharing" in index_map, "bank index routes multi-agent work to ops"
    assert "per-track" in plan, "plan splits mixed jobs by track"
    assert "never the procedure text" in area_maps["ops-index"], "ops keeps humans on dashboards"
    assert "never the runbook text" in area_maps["sec-index"], "sec keeps humans on finding counts"
    status, _, body = kget("/api/skill/verify-layout?fields=prompt")
    layout = json.loads(body)["skill"]["prompt"]
    assert "1.4.10" in layout, "layout proof cites the WCAG Reflow rulebook"
    assert "bounding box" in layout, "layout proof measures, never eyeballs alone"
    assert "overrules the skill" in layout, "user taste overrules the skill"
    status, _, body = kget("/api/skill/ops-observe?fields=prompt")
    assert "trigger event" in json.loads(body)["skill"]["prompt"], "alerts double as machine triggers"
    assert "MCP" in json.loads(body)["skill"]["prompt"], "observe prefers queryable signals over dashboards"
    assert "only witness to its own health" in json.loads(body)["skill"]["prompt"], "observe keeps an independent check"
    status, _, body = kget("/api/skill/ops-coordinate?fields=prompt")
    coord = json.loads(body)["skill"]["prompt"]
    assert "claim a task" in coord, "coordination runs on a shared plan ledger"
    assert "ops-coordinate" in area_maps["ops-index"], "ops-index routes multi-agent work"
    all_ids = [s["id"] for s in bank]
    assert len(all_ids) == len(set(all_ids)), "bank ids unique, no duplicate skills"
    routers = {"bank": index_map, "ui": ui_map, "widgets": widgets_map, **area_maps}
    for name, text in routers.items():
        assert "Skip everything else" in text, f"{name} router selects matched skills only"
    assert "always read these: code-secure, code-reuse, code-token" in index_map, "always-on set is exactly three skills"
    assert "install it, then use it locally" in index_map, "missing skills installed once, then reused"
    assert "file if longer or interruptible" in plan, "long plans persist to a file"
    lifecycle = {
        "start": ["code-index", "ui-index", "code-plan"],
        "always": ["code-secure", "code-reuse", "code-token"],
        "build": ["code-language", "code-shape", "code-group", "code-legacy", "code-lifecycle", "code-polyglot", "code-boundaries"],
        "interface": ["ui-shell", "ui-framework", "ui-widgets", "ui-forms", "ui-nav", "ui-a11y"],
        "product": ["app-index", "code-billing", "code-auth", "code-auditlog"],
        "data": ["data-index", "data-collect", "data-ingest", "data-model", "data-contracts", "data-metrics", "data-pii", "data-orchestrate"],
        "ship": ["ops-index", "ops-pipeline", "ops-observe", "ops-rollout", "ops-backup", "ops-coordinate", "ops-safety"],
        "verify": ["verify-tests", "verify-visual", "verify-layout", "verify-debug", "verify-benchmark"],
    }
    missing = [s for stage in lifecycle.values() for s in stage if s not in all_ids]
    assert not missing, f"lifecycle stages uncovered: {missing}"
    assert "code-legacy" in index_map and "code-lifecycle" in index_map, "bank routes legacy and lifecycle"
    assert "verify-debug" in index_map and "verify-benchmark" in index_map, "bank routes debug and benchmark"
    assert "ui-a11y" in ui_map, "interface map routes the a11y audit"
    assert "ops-safety" in area_maps["ops-index"], "ops map routes blast-radius safety"
    assert "data-metrics" in area_maps["data-index"] and "data-pii" in area_maps["data-index"], "data map routes metrics and PII"
    for sid, needle in [("ops-coordinate", "scoped credentials"), ("ops-safety", "human's approval first"), ("ops-secrets", "out of band"),
                        ("code-auditlog", "Name the agent"), ("data-ingest", "pass additive"),
                        ("data-quality", "name an owner and an action"), ("data-retain", "shredding"),
                        ("ops-backup", "erasure log"), ("ops-rollout", "declared by a human"),
                        ("ops-pipeline", "real bus"), ("data-contracts", "handshake"),
                        ("verify-tests", "Quarantine flakes"), ("ui-forms", "at the field"),
                        ("ui-behavior", "offline"), ("ui-tokens", "prefers-color-scheme"),
                        ("data-cdc", "watches the tap"), ("ops-rollout", "roll forward stateful")]:
        status, _, rb = kget(f"/api/skill/{sid}?fields=prompt")
        assert needle in json.loads(rb)["skill"]["prompt"], f"{sid} carries: {needle}"
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "script"))
    import bench
    m = bench.measure()
    assert m["bank_skills"] == 102, "bench sees the whole bank"
    assert all(v["share"] <= 0.20 for v in m["packs"].values()), "typical task packs stay under a fifth of the bank"
    status, _, body = get("/")
    home2 = body.decode()
    assert "owns the blast radius" in home2, "home names the fifth verdict"
    assert "13 to 17 percent" in home2, "home proof cites measured pack share"
    assert "verify-benchmark" in home2, "home proof names the trial protocol"
    assert "What the pack arms added was completeness" in home2, "home proof reports the trial honestly"
    assert "coordination-heavy build" in home2, "home proof names the discriminating follow-up"
    assert "Pay once, use forever" in home2, "home states the one-time price"
    assert 'rel="icon"' in home2 and "/brand/favicon.png" in home2, "favicon wired"
    assert "prefers-reduced-motion" in home2 and ":focus-visible" in home2, "global a11y guards present"
    assert 'property="og:image"' in home2 and "/brand/og-card.png" in home2, "social card wired"
    status, _, body = get("/code")
    assert "motion-safe:transition-transform" in body.decode(), "motion honors reduced-motion"
    status, headers, body = get("/brand/og-card.png")
    assert status == 200 and any("image/png" in v for v in headers.values()), "brand asset served"
    status, _, _ = get("/brand/evil.png")
    assert status == 404, "brand route safelisted"
    status, headers, _ = get("/brand/hero-mark.jpg")
    assert status == 200 and any("image/jpeg" in v for v in headers.values()), "header mark served"
    status, _, _ = get("/brand/banner-code.jpg")
    assert status == 404, "retired banners stay 404"
    status, _, _ = get("/brand/hero-mark.png")
    assert status == 404, "unsafelisted names stay 404 even when the file exists on disk"
    assert 'href="#content"' in home2 and 'id="content"' in home2, "skip link targets main"
    assert "min-h-[44px]" in home2, "touch targets hit 44px"
    status, _, body = get("/skills")
    assert status == 200 and 'aria-live="polite"' in body.decode(), "copy feedback announced via live region"
    assert "max-w-[1200px]" in home2 and "1060" not in home2, "container matches 1200 spec"
    assert "/brand/hero-mark.jpg" in home2, "header carries the brand mark"
    assert "Kaiti" in home2 and "text-accent" in home2, "Love set big in brush script"
    for leaf in ("/", "/code", "/ui", "/data", "/ops", "/skills", "/about", "/releases"):
        status, _, body = get(leaf)
        assert status == 200 and "banner-" not in body.decode(), f"{leaf} ships no decorative banner"
    assert "Keys open soon" in home2, "home is honest the key system is pending"
    status, _, body = get("/ops")
    assert "probabilistic actors" in body.decode(), "ops page names the deterministic-gates architecture"
    status, _, body = get("/data")
    assert "meaning stays human" in body.decode(), "data page keeps meaning with people"
    status, _, body = get("/ui")
    assert "shapes feel" in body.decode(), "ui guide keeps humans in the middle"
    assert "shaping bugs only show in real rendering" in body.decode(), "ui guide notes complex-script shaping"
    status, _, body = get("/code")
    assert "guideline 4.2" in body.decode(), "code guide warns on store rejection"
    status, _, body = get("/ops")
    ops = body.decode()
    assert "modelcontextprotocol.io" in ops, "ops page backlinks the MCP source"
    assert "Don&#x27;t trust the system" in ops or "Don't trust the system" in ops, "ops page states the verify principle"
    assert "ops-coordinate" in ops, "ops page names the coordination skill"
    assert "lease endpoint" in ops, "ops page states claims are leases"
    status, _, rb = kget("/api/skill/ops-coordinate?fields=prompt")
    assert "409" in json.loads(rb)["skill"]["prompt"], "coordination honors the lease rejection"
    status, _, rb = kget("/api/skill/ops-rollout?fields=prompt")
    assert "halt if errors exceed baseline" in json.loads(rb)["skill"]["prompt"], "rollout comparator halts on regression"
    status, _, body = post("/api/plan/claim", {"task": "t1", "agent": "a1", "ttl": "60"})
    assert status == 200, f"first claim wins, got {status}"
    status, _, body = post("/api/plan/claim", {"task": "t1", "agent": "a2"})
    assert status == 409 and "a1" in body.decode(), "second claim rejected naming the holder"
    status, _, body = post("/api/plan/release", {"task": "t1", "agent": "a2"})
    assert status == 403, f"only the holder releases, got {status}"
    status, _, body = post("/api/plan/release", {"task": "t1", "agent": "a1"})
    assert status == 200, f"holder releases, got {status}"
    status, _, body = post("/api/plan/claim", {"task": "t2", "agent": "a1", "ttl": "0"})
    assert status == 200, f"zero-ttl claim lands, got {status}"
    status, _, body = post("/api/plan/claim", {"task": "t2", "agent": "a2"})
    assert status == 200, f"expired lease is reclaimable, got {status}"
    status, _, body = get("/api/plan/claims")
    assert "t2" in body.decode(), "claims list visible"
    status, _, body = get("/signatures.json")
    assert status == 200, f"signatures served, got {status}"
    sigs = json.loads(body)
    assert sigs["bank_version"] == "1.0.0" and sigs["algorithm"] == "Ed25519", "signature set versioned and named"
    status, _, body = get("/releases")
    assert status == 200 and "v1.0.0" in body.decode(), "releases page lists the pinned bank version"
    status, _, body = get("/releases.xml")
    feed = body.decode()
    assert status == 200 and feed.startswith("<?xml") and "<rss" in feed, "release feed is valid RSS"
    assert feed.count("<item>") == 5, "feed carries every release note"
    assert "One call installs the whole bank" in home2, "install prompt leads with the key flow"
    assert "Taste free" in home2, "free tasting path stays visible"
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature
    pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(sigs["public_key"]))
    status, _, body = kget("/api/skills?fields=id,prompt,why,checks,tokens")
    for s in json.loads(body)["skills"]:
        payload = json.dumps({k: s[k] for k in ("id", "prompt", "why", "checks", "tokens")}, sort_keys=True, separators=(",", ":")).encode()
        try:
            pub.verify(bytes.fromhex(sigs["skills"][s["id"]]), payload)
        except InvalidSignature:
            raise AssertionError(f"signature mismatch (re-sign the bank): {s['id']}")
    assert len(sigs["skills"]) == 102, "every skill signed"
    bad = dict(json.loads(body)["skills"][0])
    bad["prompt"] += "tampered"
    payload = json.dumps({k: bad[k] for k in ("id", "prompt", "why", "checks", "tokens")}, sort_keys=True, separators=(",", ":")).encode()
    try:
        pub.verify(bytes.fromhex(sigs["skills"][bad["id"]]), payload)
        raise SystemExit("tampered skill verified — fail closed broken")
    except InvalidSignature:
        pass
    assert "signature" in json.loads(rb := kget("/api/skill/code-lifecycle?fields=prompt")[2])["skill"]["prompt"], "lifecycle skill verifies signatures"
    status, _, body = kget("/api/skill/ops-pipeline?fields=prompt")
    assert "trigger events" in json.loads(body)["skill"]["prompt"], "deploys broadcast machine triggers"
    status, _, body = kget("/api/skill/ui-seo?fields=prompt")
    assert "noindex" in json.loads(body)["skill"]["prompt"], "paid pages stay out of crawlers"
    status, _, body = kget("/api/skills?fields=id,prompt")
    bank_ids = [s["id"] for s in json.loads(body)["skills"]]
    prompts = {s["id"]: s["prompt"] for s in json.loads(body)["skills"]}
    index_ids = {"code-index", "ui-index", "app-index", "data-index", "ops-index", "sec-index"}
    refs = {i: [j for j in bank_ids if j != i and re.search(r"(?<![a-z0-9-])" + re.escape(j) + r"(?![a-z0-9-])", prompts[i])] for i in bank_ids}
    for k, v in refs.items():
        if k not in index_ids:
            assert not (set(v) & index_ids), f"{k} points back at an index — references flow downward only"
    color = {}
    def visit(u, stack):
        color[u] = 1
        stack.append(u)
        for w in refs[u]:
            if w in index_ids:
                continue
            if color.get(w) == 1:
                raise AssertionError("reference loop: " + " -> ".join(stack + [w]))
            if w not in color:
                visit(w, stack)
        stack.pop()
        color[u] = 2
    for i in bank_ids:
        if i not in color and i not in index_ids:
            visit(i, [])
    status, _, body = get("/")
    assert status == 200 and 'id="menubtn"' in body.decode(), "mobile hamburger present"
    status, _, _ = get("/skills.json")
    assert status == 404, "slim index endpoint is gone; board.json is the one JSON"
    status, _, body = kget("/api/skills?fields=id,prompt")
    for s in json.loads(body)["skills"]:
        assert s["prompt"].startswith("Create and install a skill named"), s["id"]
    status, _, body = kget("/api/skill/ui-shell?fields=prompt,checks")
    shell = json.loads(body)["skill"]
    assert "aria-label" in shell["prompt"] and "icon-only" in shell["prompt"], "ui-shell allows human UI + metadata"
    assert "360px" in shell["prompt"] and "360px" in shell["checks"][0], "ui-shell is mobile-first"
    assert "Lucide" in shell["prompt"], "ui-shell names Lucide, no hand SVG"
    assert any("aria-label" in c for c in shell["checks"]), "metadata check present"
    assert any("data-action" in c for c in shell["checks"]), "data-action check present"
    status, _, body = kget("/api/skill/verify-visual?fields=prompt")
    visual = json.loads(body)["skill"]
    assert "shots/" in visual["prompt"], "verify-visual saves screenshots to shots/"
    assert "headless" in visual["prompt"], "verify-visual never trusts headless shots alone"

    status, _, body = get("/skills")
    assert status == 200, f"skills page renders, got {status}"
    assert "<h1" in body.decode() and ">Skills<" in body.decode(), "page renamed to Skills"
    import http.client as _hc
    _conn = _hc.HTTPConnection("localhost", int(PORT))
    _conn.request("GET", "/board")
    _r = _conn.getresponse()
    assert _r.status == 302 and _r.getheader("Location") == "/skills", "/board redirects to /skills"
    _conn.close()
    html = body.decode()
    assert "code-reuse" in html and "Reuse before you build" in html, "skills page lists skills"
    assert "code-index" in html and "progressive disclosure" in html, "index skill maps tasks to skills"
    assert "code-ssrf" in html and "code-crypto" in html, "OWASP set renders on page"
    assert all(g in html for g in ("Start here", "Always on", "Security deep-dives", "Verify", "Run well")), "skills page groups skills"
    assert html.count("data-copy-skill=") == 102, "every skill renders exactly once"
    assert "data-copy-skill" in html, "page has copy buttons"
    assert html.count("data-trim=") == 102, "every card trimmable"
    assert "data-pack" in html and "copy install pack" in html, "trim pack builder present"
    assert "install only what matches" in html, "page pitches install-matched, not the playbook"
    assert "One hundred two skills" in html, "skills page states the live count"
    assert "nothing orphaned, nothing twice" in html, "skills page states reachability without details"
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
    status, _, _ = get("/skills")
    assert status == 200, "page views still render"
    status, _, _ = kget("/board.json")
    status, _, _ = kget("/api/skills?track=code")
    status, _, _ = kget("/api/skill/code-language?fields=id")
    status, _, body = get("/skills")
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
    status, _, body = get("/skills")
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
    assert "agentic ops" in home, "homepage frames old way versus agentic ops"
    assert "Industry zombies" in home, "homepage buries MVC/MVP fences"
    status, _, body = get("/ui")
    assert status == 200 and "Flowbite" in body.decode(), "guide names Flowbite for components"
    assert "60-30-10" in body.decode() and "Green confirms" in body.decode(), "guide teaches research-backed color rules"
    assert "combo box" in body.decode() and "300–500ms" in body.decode(), "guide teaches research-backed component rules"
    assert "jasonformat.com/islands-architecture" in body.decode(), "guide credits the islands rulebook"
    assert "Reflow (1.4.10)" in body.decode(), "guide cites WCAG Reflow for layout"
    for m in re.finditer(r'<a href="(http[^"]*)"', body.decode()):
        assert 'target="_blank" rel="noopener"' in body.decode()[m.start():m.start()+400], f"external link opens new tab: {m.group(1)}"
    status, _, body = get("/code")
    assert status == 200 and "Framework first" in body.decode(), "guide states framework-first rule"
    assert "docs.python.org" in body.decode(), "guide backs Python with the language reference"
    assert "one declaration replaces three" in body.decode() and "one contract, not one per language" in body.decode(), "guide states why each guardrail was chosen"
    assert "preflight stays on" in body.decode(), "guide states preflight-on baseline"
    assert 'target="_blank" rel="noopener"' in body.decode(), "external links open a new tab"
    status, _, body = get("/data")
    assert status == 200 and "exactly once" in body.decode(), "data guide teaches idempotent landing"
    assert "dead-letter" in body.decode(), "data guide names the poison path"
    assert "verdict layer" in body.decode(), "data guide frames old way versus new way"
    assert "vega.github.io/vega-lite" in body.decode(), "data guide backlinks the declarative spec source"
    assert "textbookofusability.com" in body.decode(), "data guide backlinks the perceptual ranking source"
    status, _, cb = kget("/api/skill/ui-charts?fields=prompt")
    charts = json.loads(cb)["skill"]["prompt"]
    assert "100% stacked" in charts, "charts skill names share-over-time explicitly"
    assert "ui-chart-twin" in charts, "picker chains the machine-twin leaf"
    status, _, tb = kget("/api/skill/ui-chart-twin?fields=prompt")
    twin = json.loads(tb)["skill"]["prompt"]
    assert "data table" in twin and "spec" in twin, "twin ships table plus spec"
    assert "Cleveland" not in charts and "W3C" not in twin, "skills carry rules, pages carry sources"
    assert "adult in the room" in body.decode(), "data guide keeps the database as arbiter"
    assert "agent readers" in body.decode(), "data guide states shapes are built for agents"
    assert "ui-charts" in ui_map, "area index routes charts"
    assert "data-model" in area_maps["data-index"], "area index routes data representation"
    status, _, body = kget("/api/skill/data-model?fields=prompt")
    assert "the change plus the id" in json.loads(body)["skill"]["prompt"], "data respects the systems it lands in"
    for m in re.finditer(r'<a href="(http[^"]*)"', body.decode()):
        assert 'target="_blank" rel="noopener"' in body.decode()[m.start():m.start()+400], f"data external link opens new tab: {m.group(1)}"
    status, _, body = get("/ops")
    assert status == 200 and "Blameless" in body.decode(), "ops guide teaches blameless reviews"
    assert "rollback" in body.decode(), "ops guide names the rollback trigger"
    for m in re.finditer(r'<a href="(http[^"]*)"', body.decode()):
        assert 'target="_blank" rel="noopener"' in body.decode()[m.start():m.start()+400], f"ops external link opens new tab: {m.group(1)}"
    status, _, body = get("/sitemap.xml")
    assert status == 200 and "/data" in body.decode() and "/ops" in body.decode(), "sitemap lists new guides"
    status, _, body = kget("/api/skill/ui-framework?fields=prompt")
    lit = json.loads(body)["skill"]
    assert "Flowbite" in lit["prompt"] and "React" in lit["prompt"], "ui-framework keeps Flowbite pieces, rules out heavy frameworks"
    assert "WebAwesome" in lit["prompt"], "ui-framework names WebAwesome for island pieces"
    status, _, body = get("/skills")
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
