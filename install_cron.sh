#!/bin/bash
# Install cron job for router restart

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_WRAPPER="$SCRIPT_DIR/router_restart_cron.sh"
PYTHON_SCRIPT="$SCRIPT_DIR/router_restart.py"
VENV_DIR="$SCRIPT_DIR/venv"

# Check if necessary files exist
if [ ! -f "$CRON_WRAPPER" ]; then
    echo "Error: Cron wrapper script not found at $CRON_WRAPPER"
    exit 1
fi

if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "Error: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please run: ./setup.sh"
    exit 1
fi

# Make scripts executable
chmod +x "$CRON_WRAPPER"
chmod +x "$PYTHON_SCRIPT"

# Create temporary crontab file
CRON_TMP=$(mktemp)

# Get current crontab (if exists)
crontab -l 2>/dev/null > "$CRON_TMP" || true

# Check if job already exists
if grep -q "$CRON_WRAPPER" "$CRON_TMP"; then
    echo "ℹ  Cron job already installed"
    rm "$CRON_TMP"
    crontab -l | grep "$CRON_WRAPPER"
    exit 0
fi

# Add new cron job (3 AM daily)
# Format: minute hour day month day_of_week command
echo "0 3 * * * $CRON_WRAPPER" >> "$CRON_TMP"

# Install crontab
crontab "$CRON_TMP"
CRON_RESULT=$?
rm "$CRON_TMP"

if [ $CRON_RESULT -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════╗"
    echo "║  ✓ CRON JOB INSTALLED SUCCESSFULLY!        ║"
    echo "╚════════════════════════════════════════════╝"
    echo ""
    echo "📅 Scheduled: Daily at 3:00 AM"
    echo "🔧 Wrapper:   $CRON_WRAPPER"
    echo "📝 Python:    $PYTHON_SCRIPT"
    echo "📦 venv:      $VENV_DIR"
    echo "📋 Logs:      ~/router_restart.log"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Useful commands:"
    echo ""
    echo "  View cron job:"
    echo "    crontab -l"
    echo ""
    echo "  View live logs:"
    echo "    tail -f ~/router_restart.log"
    echo ""
    echo "  Test manually:"
    echo "    $CRON_WRAPPER"
    echo ""
    echo "  Remove cron job:"
    echo "    crontab -r"
    echo ""
else
    echo "Error: Failed to install cron job"
    exit 1
fi
