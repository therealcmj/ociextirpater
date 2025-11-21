
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
DELAY=60

echo "#### Creating Extirpater user: $USER ####"
useradd --system -M $USER

# Function to attempt a command with retries
attempt_with_retry() {
  local attempt=0
  local command="$1"
  while [ $attempt -lt $MAX_ATTEMPTS ]; do
    if $command; then
      return 0
    else
      echo "Failed. Retrying in 5 seconds..."
      sleep $TIMEOUT
      attempt=$((attempt + 1))
    fi
  done
  echo "Failed after $MAX_ATTEMPTS attempts."
  return 1
}

# Delay for normalization before network operations
echo "#### Sleeping $DELAY seconds ####"
sleep $DELAY

# Oracle Autonomous Linux 9
echo "#### Installing git ####"
attempt_with_retry "sudo yum install -y git"
if [ $? -eq 1 ]; then
  exit 1
fi

echo "#### Cloning Extirpater Repository ####"
attempt_with_retry "git clone --depth 1 https://github.com/therealcmj/ociextirpater.git $EXT_DIR"
if [ $? -eq 1 ]; then
  exit 1
fi
chown -R root:$USER $EXT_DIR
chmod -R 750 $EXT_DIR
git config --system --add safe.directory $EXT_DIR

echo "#### Setting Executables: $EXT_DIR/deploy/scripts/daily.sh ####"
chown root:$USER $EXT_DIR/deploy/scripts/daily.sh
chmod 750 $EXT_DIR/deploy/scripts/daily.sh

# Tested with Python 3.9.21
echo "#### Creating Virtual Environment: $VENV ####"
attempt_with_retry "python -m venv $VENV"
if [ $? -eq 1 ]; then
  exit 1
fi

echo "#### Getting Dependencies ####"
# Upgrading pip is not a hard requirement but a nice to have
attempt_with_retry "$VENV/bin/pip install --upgrade pip"
attempt_with_retry "$VENV/bin/pip install -r $EXT_DIR/requirements.txt"
if [ $? -eq 1 ]; then
  exit 1
fi

echo "#### Making Log Directory: $LOG_DIR ####"
mkdir -p $LOG_DIR
chown $USER:$USER $LOG_DIR
chmod 2750 $LOG_DIR
semanage fcontext -a -t var_log_t '/var/log/ociextirpater(/.*)?'
restorecon -Rv /var/log/ociextirpater

echo "#### Setting Crontab ####"
echo "0 0 * * * $EXT_DIR/deploy/scripts/daily.sh $TOBEDELETED $LOG_DIR $EXT_TAG" > cron.txt
crontab -u $USER cron.txt
echo "#### Crontab $(crontab -u $USER -l) ####"
