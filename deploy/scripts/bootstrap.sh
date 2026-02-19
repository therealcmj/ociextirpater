
set -Eeo pipefail
IFS=$'\n\t'
umask 0027
[ "$(id -u)" -eq 0 ] || { echo "Run as root"; exit 1; }

# $TOBEDELETED required to be set
if [ -v TOBEDELETED ]; then echo "#### Extirpate Compartment $TOBEDELETED ####"
else echo "#### ERROR: No compartment set ####" && exit 1
fi

# Variables
EXT_DIR=/usr/local/ociextirpater
VENV=$EXT_DIR/.venv
LOG_DIR=/var/log/ociextirpater
MAX_ATTEMPTS=5
TIMEOUT=5
USER=extirpate
DELAY=150

echo "#### Ensuring service user: $USER ####"
if ! id -u "$USER" >/dev/null 2>&1; then
  getent group "$USER" >/dev/null 2>&1 || groupadd --system "$USER"
  useradd --system -m -d "/var/lib/${USER}" -s /sbin/nologin -g "$USER" "$USER"
fi
echo "#### Complete ####"

# Function to attempt a command with retries
attempt_with_retry() {
  local max="${MAX_ATTEMPTS:-5}"
  local delay="${TIMEOUT:-5}"
  local attempt=1
  while true; do
    "$@"
    local rc=$?
    if [ "$rc" -eq 0 ]; then
      return 0
    fi
    if [ "$attempt" -ge "$max" ]; then
      echo "Failed after ${attempt}/${max} attempts (rc=$rc)." >&2
      return "$rc"
    fi
    echo "Attempt ${attempt}/${max} failed (rc=$rc). Retrying in ${delay}s..." >&2
    sleep "$delay"
    delay=$((delay * 2))
    attempt=$((attempt + 1))
  done
}

# Delay for normalization before network operations
echo "#### Sleeping $DELAY seconds ####"
sleep $DELAY
echo "#### Complete ####"

# Oracle Autonomous Linux 9
echo "#### Installing prerequisites ####"
if command -v dnf >/dev/null 2>&1; then
  PKG_MGR=dnf
  echo "  ## Using dnf package manager ##  "
  attempt_with_retry dnf -y --refresh makecache
  attempt_with_retry dnf -y --setopt=retries=10 --setopt=metadata_expire=0 --setopt=timeout=30 install git python3 python3-pip policycoreutils-python-utils
else
  PKG_MGR=yum
    echo "  ## Using yum package manager ##  "
  attempt_with_retry yum -y makecache
  attempt_with_retry yum -y --setopt=retries=10 --setopt=metadata_expire=0 --setopt=timeout=30 install git python3 python3-pip policycoreutils-python-utils
fi
echo "#### Complete ####"

echo "#### Cloning Extirpater Repository ####"
install -d -o "$USER" -g "$USER" -m 0755 "$(dirname "$EXT_DIR")"
if command -v runuser >/dev/null 2>&1; then
  attempt_with_retry runuser -u "$USER" -- git clone --depth 1 https://github.com/therealcmj/ociextirpater.git "$EXT_DIR"
else
  attempt_with_retry su -s /bin/sh -c "git clone --depth 1 https://github.com/therealcmj/ociextirpater.git '$EXT_DIR'" "$USER"
fi
chown -R "$USER:$USER" "$EXT_DIR"
chmod -R g+rx "$EXT_DIR"

echo "#### Setting Executables: $EXT_DIR/deploy/scripts/daily.sh ####"
chown root:$USER $EXT_DIR/deploy/scripts/daily.sh
chmod 750 $EXT_DIR/deploy/scripts/daily.sh

echo "#### Complete ####"

# Tested with Python 3.9.21
echo "#### Creating Virtual Environment: $VENV ####"
if command -v runuser >/dev/null 2>&1; then
  attempt_with_retry runuser -u "$USER" -- python3 -m venv "$VENV"
else
  attempt_with_retry su -s /bin/sh -c "python3 -m venv '$VENV'" "$USER"
fi
echo "#### Complete ####"

echo "#### Getting Dependencies ####"
attempt_with_retry runuser -u "$USER" -- "$VENV/bin/pip" install --upgrade pip
attempt_with_retry runuser -u "$USER" -- "$VENV/bin/pip" install -r "$EXT_DIR/requirements.txt"
echo "#### Complete ####"

echo "#### Making Log Directory: $LOG_DIR ####"
install -d -o "$USER" -g "$USER" -m 2750 "$LOG_DIR"
if command -v getenforce >/dev/null 2>&1 && [ "$(getenforce)" != "Disabled" ]; then
  command -v semanage >/dev/null 2>&1 || { if [ "${PKG_MGR:-}" = "dnf" ]; then attempt_with_retry dnf -y install policycoreutils-python-utils || true; else attempt_with_retry yum -y install policycoreutils-python-utils || true; fi; }
  semanage fcontext -a -t var_log_t '/var/log/ociextirpater(/.*)?' || true
  restorecon -Rv /var/log/ociextirpater || true
fi
echo "#### Complete ####"

echo "#### Setting Crontab ####"
CRON_TMP=$(mktemp)
{
  echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$VENV/bin"
  echo "0 0 * * * $EXT_DIR/deploy/scripts/daily.sh $TOBEDELETED $LOG_DIR $EXT_TAG"
} > "$CRON_TMP"
crontab -u $USER "$CRON_TMP"
rm -f "$CRON_TMP"
echo "#### Crontab $(crontab -u $USER -l) ####"
echo "#### Complete ####"
