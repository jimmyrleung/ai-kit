#!/usr/bin/env bash
# Compatibility wrapper. The common Python engine owns all enumeration and mutation.
set -euo pipefail

if [[ ${CURSOR_HOME+x} ]]; then
  echo "CURSOR_HOME is not accepted by the common sync; use --home for an isolated user base." >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/../../scripts/sync-skills.py" "$@"
