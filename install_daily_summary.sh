#!/bin/bash
# Installs the daily summary emailer as a macOS launchd agent (runs at 8pm daily)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.user.macbook-price-tracker-daily"
PLIST_SRC="$SCRIPT_DIR/$PLIST_NAME.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
LOG_DIR="$SCRIPT_DIR"

PYTHON=$(command -v python3 || true)
if [ -z "$PYTHON" ]; then
    echo "❌  Python 3 not found."
    exit 1
fi

sed \
    -e "s|PYTHON_PATH|$PYTHON|g" \
    -e "s|SCRIPT_PATH|$SCRIPT_DIR/daily_summary.py|g" \
    -e "s|LOG_PATH|$LOG_DIR|g" \
    "$PLIST_SRC" > "$PLIST_DEST"

echo "✓ Plist written to $PLIST_DEST"

launchctl unload "$PLIST_DEST" 2>/dev/null || true
launchctl load "$PLIST_DEST"

echo "✓ Daily summary agent loaded — email will be sent every day at 8:00 PM"
echo ""
echo "Test it right now with:  python3 $SCRIPT_DIR/daily_summary.py"
