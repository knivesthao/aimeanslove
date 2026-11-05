"""Open endpoints + usage tracking. Run: .venv/bin/python test/api_test.py"""
import json
import os
import re
import subprocess
import sys
import time
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


child = subprocess.Popen(
    [sys.executable, "server.py"],
    cwd=ROOT,
    env={**os.environ, "PORT": PORT, "USAGE_FILE": USAGE_FILE},
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
    assert len(bank) == 14 and all(s.get("why") for s in bank), "every skill explains why"
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
    assert any("aria-label" in c for c in shell["checks"]), "metadata check present"
    assert any("data-action" in c for c in shell["checks"]), "data-action check present"

    status, _, body = get("/board")
    assert status == 200, f"board renders, got {status}"
    html = body.decode()
    assert "ui-details" in html and "Collapsible card stacks" in html, "board lists skills"
    assert "data-copy-skill" in html, "board has copy buttons"
    assert 'id="q"' not in html and "data-track" not in html, "no filter machinery"
    assert "/llms.txt" not in html and "/api/stats" not in html, "no machine links on human pages"
    status, _, body = get("/board.json")
    assert status == 200
    status, _, body = get("/api/skills")
    assert status == 200
    status, _, body = get("/board")
    html = body.decode()
    m = re.search(r"Our library has been used (\d+) (time|times)\.", html)
    assert m, "board shows usage counter"
    assert int(m.group(1)) >= 2, f"counter reflects bank fetches, got {m.group(0)}"
    print("PASS: open endpoints + usage stats + board")
finally:
    child.terminate()
