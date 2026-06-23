#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/common.env"

: "${EXT_DIR:?EXT_DIR must be set by common.env}"
: "${LOG_DIR:?LOG_DIR must be set by common.env}"

# Variables
VENV=$EXT_DIR/.venv
CURRENT_DT=$(date +%Y-%m-%d)

# Update oci
"$VENV/bin/pip" install --upgrade pip oci

git -C "$EXT_DIR" pull origin main
"$VENV/bin/python" "$EXT_DIR/ociextirpate.py" -ip -force -c "$1" \
-log "$LOG_DIR/$CURRENT_DT.log" -skip_tagged "$2"
