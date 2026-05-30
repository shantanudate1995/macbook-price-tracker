# MacBook Air Price Tracker

Monitors the **MacBook Air 13" M5 base model** on Best Buy Canada and alerts you via Mac notification + Gmail when the price drops below **$1,499 CAD**.

Runs silently in the background every hour via macOS `launchd`. Survives reboots.

---

## Setup (one time, ~2 minutes)

### 1. Get a Gmail App Password
1. Go to https://myaccount.google.com/apppasswords
2. Name it "Price Tracker" → click **Create**
3. Copy the 16-character password

### 2. Open Terminal and run:

```bash
cd ~/macbook-price-tracker
python3 setup.py
```

Enter your Gmail address and the app password when prompted. It will verify the connection.

### 3. Install the background agent:

```bash
bash install_launchd.sh
```

That's it. The tracker is now running every hour in the background.

---

## Test it manually

```bash
python3 check_price.py
```

---

## View logs

```bash
tail -f ~/macbook-price-tracker/price_tracker.log
```

---

## Stop / uninstall

```bash
# Stop (keeps files)
launchctl unload ~/Library/LaunchAgents/com.user.macbook-price-tracker.plist

# Remove entirely
rm ~/Library/LaunchAgents/com.user.macbook-price-tracker.plist
```

---

## Files

| File | Purpose |
|---|---|
| `check_price.py` | Main script — fetches price, sends alerts |
| `setup.py` | One-time config wizard |
| `install_launchd.sh` | Installs the hourly background job |
| `config.json` | Your Gmail credentials (created by setup.py) |
| `last_price.json` | Last seen price (auto-created) |
| `price_tracker.log` | Output log |
