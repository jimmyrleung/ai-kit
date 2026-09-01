#!/usr/bin/env bash
# Compatibility wrapper. The common Python engine owns all enumeration and mutation.
set -euo pipefail

if [[ -v CODEX_HOME ]]; then
  echo "CODEX_HOME is not accepted by the common sync; use --home for an isolated user base." >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/../../scripts/sync-skills.py" "$@"
