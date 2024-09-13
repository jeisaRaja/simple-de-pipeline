#!/bin/bash
echo "Start Luigi ETL Pipeline Process"
PROJECT_DIR="$(dirname "$(realpath "$0")")"

VENV_PATH="$PROJECT_DIR/venv/bin/activate"
source "$VENV_PATH"

PYTHON_SCRIPT="$PROJECT_DIR/etl.py"

LOG_DIR="$PROJECT_DIR/logs"
LOGFILE="$LOG_DIR/logfile.log"
LUIGI_LOG="$LOG_DIR/luigi_start.log"

if pgrep -x "luigid" > /dev/null
then
    echo "luigid is already running."
else
    echo "Starting luigid..."
    luigid --port 8082 &
fi

echo "Luigi Started at ${dt}" >> "$LUIGI_LOG"

python3 "$PYTHON_SCRIPT" >> "$LOGFILE" 2>&1

dt=$(date '+%d/%m/%Y %H:%M:%S');

echo "End Luigi ETL Pipeline Process"
