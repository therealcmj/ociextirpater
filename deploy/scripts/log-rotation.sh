#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=/dev/null
source "$SCRIPT_DIR/common.env"

: "${LOG_DIR:?LOG_DIR must be set by common.env}"
: "${COMPRESS_AFTER_DAYS:?COMPRESS_AFTER_DAYS must be set by common.env}"
: "${RETENTION_DAYS:?RETENTION_DAYS must be set by common.env}"

today="$(date +%F)"
compress_before="$(date -d "-${COMPRESS_AFTER_DAYS} days" +%F)"
delete_before="$(date -d "-${RETENTION_DAYS} days" +%F)"

[ -d "$LOG_DIR" ] || exit 0

if (( RETENTION_DAYS <= COMPRESS_AFTER_DAYS )); then
    echo "RETENTION_DAYS must be greater than COMPRESS_AFTER_DAYS" >&2
    exit 1
fi

# Compress completed logs older than COMPRESS_AFTER_DAYS.
# Example:
#   if today is 2026-06-01, logs dated 2026-05-02 or newer stay uncompressed.
#   logs dated 2026-05-01 or older are compressed.
find "$LOG_DIR" -maxdepth 1 -type f -name '????-??-??.log' -print0 |
while IFS= read -r -d '' file; do
    base="$(basename "$file")"

    [[ "$base" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.log$ ]] || continue

    log_date="${base%.log}"

    # Leave today's log and the last 30 days uncompressed.
    if [[ "$log_date" < "$compress_before" ]]; then
        gzip -n -- "$file"
    fi
done

# Delete compressed logs older than RETENTION_DAYS.
find "$LOG_DIR" -maxdepth 1 -type f -name '????-??-??.log.gz' -print0 |
while IFS= read -r -d '' file; do
    base="$(basename "$file")"

    [[ "$base" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.log\.gz$ ]] || continue

    log_date="${base%.log.gz}"

    if [[ "$log_date" < "$delete_before" ]]; then
        rm -f -- "$file"
    fi
done
