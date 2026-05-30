#!/bin/bash
# Installs the price tracker as a macOS launchd agent (runs hourly, survives reboots)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.user.macbook-price-tracker"
PLIST_SRC="$SCRIPT_DIR/$PLIST_NAME.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME.plist"
LOG_DIR="$SCRIPT_DIR"

# Detect Python 3
PYTHON=$(command -v python3 || true)
if [ -z "$PYTHON" ]; then
    echo "❌  Python 3 not found. Install it from https://python.org or via Homebrew: brew install python3"
    exit 1
fi
echo "✓ Using Python: $PYTHON"

# Fill in paths in the plist
sed \
    -e "s|PYTHON_PATH|$PYTHON|g" \
    -e "s|SCRIPT_PATH|$SCRIPT_DIR/check_price.py|g" \
    -e "s|LOG_PATH|$LOG_DIR|g" \
    "$PLIST_SRC" > "$PLIST_DEST"

echo "✓ Plist written to $PLIST_DEST"

# Unload if already loaded (ignore errors)
launchctl unload "$PLIST_DEST" 2>/dev/null || true

# Load the agent
launchctl load "$PLIST_DEST"
echo "✓ launchd agent loaded — price will be checked every hour"
echo ""
echo "Useful commands:"
echo "  Check logs:      tail -f $LOG_DIR/price_tracker.log"
echo "  Run manually:    python3 $SCRIPT_DIR/check_price.py"
echo "  Stop tracking:   launchctl unload $PLIST_DEST"
echo "  Remove entirely: rm $PLIST_DEST"
