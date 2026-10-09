#!/usr/bin/env bash
# Boot a throwaway altero instance for end-to-end testing, optionally with the
# lab Zotero Desktop client pointed at it. Scratch state lives in $SCRATCH and
# can be deleted wholesale after a run.
#
#   tools/dev-e2e.sh              start server on :8085 with a fresh database
#   tools/dev-e2e.sh --client     also launch the lab Zotero client
#   SCRATCH=/tmp/x PORT=9000 tools/dev-e2e.sh
#
# The first run provisions user `pilot` (no password) and prints an API key
# (user scope) plus one with group scope. Give the key to the client via
# Zotero's login, or in-console:
#   Zotero.Sync.Runner.backgroundSync = true;
#   Zotero.Sync.Runner.apiKey = '<key>';

set -euo pipefail

PORT="${PORT:-8085}"
SCRATCH="${SCRATCH:-/tmp/altero-dev-e2e}"
CLIENT_DIR="${CLIENT_DIR:-$HOME/zotero-lab/Zotero_linux-x86_64}"
PROFILE="${PROFILE:-$HOME/zotero-lab/profile}"

cd "$(dirname "$0")/.."
mkdir -p "$SCRATCH"
export ALTERO_DATABASE_URL="sqlite+aiosqlite:///$SCRATCH/altero.sqlite"
export ALTERO_PORT="$PORT"

if [ ! -s "$SCRATCH/altero.sqlite" ]; then
    uv run alembic upgrade head
    uv run altero user add pilot --display-name "E2E Pilot"
    echo "== user-scope key:"
    uv run altero key add pilot --name user-scope
    echo "== group-scope key:"
    uv run altero key add pilot --name group-scope --groups
fi

cleanup() {
    [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT

uv run altero serve &
SERVER_PID=$!
echo "== altero on http://127.0.0.1:$PORT (pid $SERVER_PID, db $SCRATCH/altero.sqlite)"

if [ "${1:-}" = "--client" ]; then
    sleep 2
    "$CLIENT_DIR/zotero" -profile "$PROFILE" -datadir "$SCRATCH/zotero-data"
else
    wait "$SERVER_PID"
fi
