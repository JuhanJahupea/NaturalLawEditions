#!/bin/sh
# Run every check: both editions against their working-edition data.json, then the link check.
# Usage: tools/check_all.sh <vattel-reuse/edition_data/data.json> <burlamaqui-reuse/edition/data.json> [<essai data.json>]
# The Essai's data.json is rebuilt from texts/vattel-loisir-1747/LOI47.json when the third path is not given.
# Needs Python 3, Node and Playwright with Chromium.
set -e
cd "$(dirname "$0")/.."
python3 -m http.server 8000 >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER' EXIT
sleep 1
node tools/check_edition.js vattel-1773 "$1"
node tools/check_edition.js burlamaqui-1747 "$2"
ESSAI="$3"
if [ -z "$ESSAI" ]; then ESSAI=$(mktemp); python3 tools/transcription/essai_data.py texts/vattel-loisir-1747/LOI47.json "$ESSAI" >/dev/null; fi
node tools/check_edition.js vattel-essai-1747 "$ESSAI"
node tools/check_links.js
