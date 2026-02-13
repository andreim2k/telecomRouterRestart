#!/bin/bash
# Install cron job for router restart

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/router_restart.py"

# Check if script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: router_restart.py not found at $SCRIPT_PATH"
    exit 1
fi

# Make script executable
chmod +x "$SCRIPT_PATH"

# Create temporary crontab file
CRON_TMP=$(mktemp)

# Get current crontab (if exists)
crontab -l 2>/dev/null > "$CRON_TMP" || true

# Check if job already exists
if grep -q "$SCRIPT_PATH" "$CRON_TMP"; then
    echo "Cron job already installed"
    rm "$CRON_TMP"
    exit 0
fi

# Add new cron job (3 AM daily)
echo "0 3 * * * $SCRIPT_PATH" >> "$CRON_TMP"

# Install crontab
crontab "$CRON_TMP"
rm "$CRON_TMP"

echo "✓ Cron job installed successfully!"
echo "✓ Router will restart daily at 3:00 AM"
echo ""
echo "View installed cron job:"
echo "  crontab -l"
echo ""
echo "View execution logs:"
echo "  tail -f /var/log/router_restart.log"
echo ""
echo "Remove cron job (if needed):"
echo "  crontab -r"
