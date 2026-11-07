#!/usr/bin/env python3
"""Mint a forever API key for the skill bank. Run: .venv/bin/python script/mint_key.py [label] [--cap N]

Prints the key ONCE — store it somewhere safe, it cannot be recovered.
Only the SHA-256 hash lands in keys.json (gitignored, server-readable).
Default cap is 10 projects per key; --cap N mints a higher-limit (e.g. team) key.
Revoke with: .venv/bin/python script/mint_key.py --revoke <key>
"""
import hashlib
import json
import os
import secrets
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
KEYS_FILE = Path(os.environ.get("AILV_KEYS_FILE", str(ROOT / "keys.json")))


def _load():
    if KEYS_FILE.exists():
        return json.loads(KEYS_FILE.read_text(encoding="utf-8"))
    return {"keys": {}}


def _save(db):
    KEYS_FILE.write_text(json.dumps(db, indent=2, sort_keys=True) + "\n")


def main():
    db = _load()
    if len(sys.argv) == 3 and sys.argv[1] == "--revoke":
        digest = hashlib.sha256(sys.argv[2].encode()).hexdigest()
        if digest in db["keys"]:
            db["keys"][digest]["active"] = False
            _save(db)
            print("revoked")
        else:
            sys.exit("unknown key")
        return
    raw_args = sys.argv[1:]
    args, cap = [], 0
    skip_next = False
    for i, a in enumerate(raw_args):
        if skip_next:
            skip_next = False
            continue
        if a == "--cap":
            try:
                cap = int(raw_args[i + 1])
            except (IndexError, ValueError):
                sys.exit("--cap needs a number")
            skip_next = True
            continue
        args.append(a)
    label = args[0] if args else ""
    raw = "ailv_" + secrets.token_urlsafe(24)
    digest = hashlib.sha256(raw.encode()).hexdigest()
    entry = {"label": label, "active": True, "uses": 0}
    if cap > 0:
        entry["cap"] = cap
    db["keys"][digest] = entry
    _save(db)
    print(raw)


if __name__ == "__main__":
    main()
