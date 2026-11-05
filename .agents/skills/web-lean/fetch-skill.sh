#!/bin/sh
# fetch-skill.sh — slim, ETag-cached skill fetch. No key needed.
# usage: MF_BASE=http://localhost:8787 ./fetch-skill.sh code-secure "prompt,checks"
set -eu
ID="${1:?skill id required}"
FIELDS="${2:-prompt,checks}"
BASE="${MF_BASE:-http://localhost:8787}"
CACHE="${MF_ETAG_DIR:-/tmp/mf-etags}"
mkdir -p "$CACHE"
SLUG=$(echo "$FIELDS" | tr -d ' ,')
TAG_FILE="$CACHE/${ID}.${SLUG}.etag"
URL="$BASE/api/skill/$ID?fields=$(echo "$FIELDS" | tr -d ' ')"
if [ -f "$TAG_FILE" ]; then
  CODE=$(curl -s -o /tmp/mf-body.json -w "%{http_code}" \
    -H "If-None-Match: $(cat "$TAG_FILE")" "$URL")
else
  CODE=$(curl -s -o /tmp/mf-body.json -w "%{http_code}" -D /tmp/mf-hdrs.txt "$URL")
fi
if [ "$CODE" = "304" ]; then
  echo "CACHED $ID (etag still valid, zero tokens)"
else
  grep -i '^etag:' /tmp/mf-hdrs.txt | awk '{print $2}' | tr -d '\r\n ' > "$TAG_FILE" || true
  echo "FRESH $ID (http $CODE, etag cached)"
  cat /tmp/mf-body.json; echo
fi
