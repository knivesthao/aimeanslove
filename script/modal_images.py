#!/usr/bin/env python3
"""Render images via the 3E Modal endpoint (SDXL-Turbo) — spend is Modal credits, not Muse credits.

Auth: MODAL_IMAGE_API_URL + MODAL_PROXY_TOKEN from env, else read from
3E's api/.dev.vars (never printed, never committed). Output goes to shots/ (gitignored).
Run: .venv/bin/python script/modal_images.py "<prompt>" <w> <h> <out.png>
   or: .venv/bin/python script/modal_images.py --batch
"""
import base64
import json
import os
import ssl
import sys
import urllib.request
from pathlib import Path

try:
    import certifi
    _CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # system trust store
    _CTX = ssl.create_default_context()

ROOT = Path(__file__).parent.parent
SHOTS = ROOT / "shots"
FALLBACK_VARS = Path("/Users/yeethao/dev/ADMAIS/3E/api/.dev.vars")

SHOTS.mkdir(exist_ok=True)

BATCH = [
    ("minimalist ink-brush mark, single loving gesture stroke, black ink on warm paper white, elegant, high contrast, centered, no text", 640, 640, "shots/hero-mark.png"),
    ("soft abstract dawn gradient background, warm paper tones with one red accent wash, calm, minimal, wide banner, no text", 1024, 576, "shots/og-bg.png"),
    ("tiny bold ink mark, single brush stroke, black on white, app icon style, centered, no text", 256, 256, "shots/favicon-mark.png"),
]


def creds():
    url = os.environ.get("MODAL_IMAGE_API_URL")
    tok = os.environ.get("MODAL_PROXY_TOKEN")
    if not (url and tok) and FALLBACK_VARS.exists():
        for line in FALLBACK_VARS.read_text().splitlines():
            k, _, v = line.partition("=")
            if k == "MODAL_IMAGE_API_URL" and not url:
                url = v.strip()
            elif k == "MODAL_PROXY_TOKEN" and not tok:
                tok = v.strip()
    if not (url and tok):
        sys.exit("need MODAL_IMAGE_API_URL + MODAL_PROXY_TOKEN (env or 3E api/.dev.vars)")
    return url, tok


def render(prompt, width, height, out):
    url, tok = creds()
    req = urllib.request.Request(
        url,
        data=json.dumps({"prompt": prompt, "width": width, "height": height, "auth": tok}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300, context=_CTX) as r:
        res = json.loads(r.read().decode())
    if "image_b64" not in res:
        sys.exit(f"render failed: {res}")
    dest = ROOT / out
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(base64.b64decode(res["image_b64"]))
    print("wrote", dest.relative_to(ROOT), dest.stat().st_size, "bytes")


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--batch":
        for prompt, w, h, out in BATCH:
            render(prompt, w, h, out)
    elif len(sys.argv) == 5:
        _, prompt, w, h, out = sys.argv
        render(prompt, int(w), int(h), out)
    else:
        sys.exit("usage: modal_images.py \"<prompt>\" <w> <h> <out> | --batch")


if __name__ == "__main__":
    main()
