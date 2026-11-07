#!/usr/bin/env python3
"""Sign the skill bank with Ed25519. Run: .venv/bin/python script/sign_bank.py [--generate]

Key: BANK_SIGNING_KEY env (base64 raw 32-byte seed) or .secrets/bank_signing.key
(0600, never committed). --generate creates one. Writes signatures.json (tracked):
{"bank_version", "algorithm", "public_key", "skills": {id: sig_hex}}.
"""
import base64
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
BANK = json.loads((ROOT / "skills.json").read_text(encoding="utf-8"))
OUT = ROOT / "signatures.json"
KEYFILE = ROOT / ".secrets" / "bank_signing.key"


def canonical(skill):
    return json.dumps(
        {k: skill[k] for k in ("id", "prompt", "why", "checks", "tokens")},
        sort_keys=True, separators=(",", ":"),
    ).encode()


def load_key():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    raw = os.environ.get("BANK_SIGNING_KEY")
    if raw:
        return Ed25519PrivateKey.from_private_bytes(base64.b64decode(raw))
    if KEYFILE.exists():
        return Ed25519PrivateKey.from_private_bytes(base64.b64decode(KEYFILE.read_text().strip()))
    sys.exit("no signing key: set BANK_SIGNING_KEY or run with --generate")


def main():
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    if "--generate" in sys.argv:
        key = Ed25519PrivateKey.generate()
        seed = base64.b64encode(key.private_bytes_raw()).decode()
        KEYFILE.parent.mkdir(exist_ok=True)
        KEYFILE.write_text(seed + "\n")
        os.chmod(KEYFILE, 0o600)
        print("wrote", KEYFILE.relative_to(ROOT), "(never commit this)")
        return
    key = load_key()
    pub = key.public_key().public_bytes_raw().hex()
    sigs = {s["id"]: key.sign(canonical(s)).hex() for s in BANK}
    version = next(
        (l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / "server.py").read_text(encoding="utf-8").splitlines() if l.startswith("BANK_VERSION = ")),
        "1.0.0",
    )
    OUT.write_text(json.dumps(
        {"bank_version": version, "algorithm": "Ed25519", "public_key": pub, "skills": sigs},
        indent=2, sort_keys=True,
    ) + "\n")
    print("signed", len(sigs), "skills ->", OUT.name)


if __name__ == "__main__":
    main()
