#!/bin/sh
# run.sh — one entry point. Foreground process: Ctrl+C stops it.
set -eu
cd "$(dirname "$0")"
cmd="${1:-dev}"
if [ ! -d .venv ]; then
  python3 -m venv .venv
  .venv/bin/pip install -r requirements.txt
fi
case "$cmd" in
  dev) exec .venv/bin/python server.py ;;
  test) exec .venv/bin/python test/api_test.py ;;
  *) echo "usage: ./run.sh [dev|test]" >&2; exit 1 ;;
esac
