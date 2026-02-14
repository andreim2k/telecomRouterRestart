#!/bin/bash
# Cron wrapper script for router restart
# This script activates the virtual environment and runs the Python script
# Called by cron at 3 AM daily

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
PYTHON_SCRIPT="$SCRIPT_DIR/router_restart.py"
LOG_FILE="$HOME/router_restart.log"

# Ensure log file exists and is writable
touch "$LOG_FILE" 2>/dev/null || true

# Log cron execution
{
    echo "=========================================="
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cron job started"
    echo "=========================================="
} >> "$LOG_FILE"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    {
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Virtual environment not found at $VENV_DIR"
        echo "Please run: cd $SCRIPT_DIR && ./setup.sh"
    } >> "$LOG_FILE"
    exit 1
fi

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    {
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: Python script not found at $PYTHON_SCRIPT"
    } >> "$LOG_FILE"
    exit 1
fi

# Activate virtual environment and run script
{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Activating virtual environment from: $VENV_DIR"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Running: $PYTHON_SCRIPT"
    echo ""
} >> "$LOG_FILE"

# Set environment for headless execution and snap applications
export DISPLAY=""
export PATH="/snap/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
mkdir -p "$XDG_RUNTIME_DIR" 2>/dev/null || true

# Run the Python script with the venv Python interpreter
source "$VENV_DIR/bin/activate"
"$VENV_DIR/bin/python3" "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1
EXIT_CODE=$?

# Log completion
{
    echo ""
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cron job completed with exit code: $EXIT_CODE"
    echo "=========================================="
    echo ""
} >> "$LOG_FILE"

exit $EXIT_CODE
