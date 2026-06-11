#!/usr/bin/env python3
"""
MacBook Air 13" M5 - Best Buy Canada Price Tracker
Checks price hourly and alerts via Mac notification + Gmail if price drops.
"""

import json
import smtplib
import subprocess
import urllib.request
from email.mime.text import MIMEText
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
PRODUCT_ID   = "19791103"
PRODUCT_URL  = f"https://www.bestbuy.ca/en-ca/product/apple-macbook-air-13-6-w-touch-id-2026-midnight-apple-m5-16gb-ram-512gb-ssd-english/{PRODUCT_ID}"
API_URL      = f"https://www.bestbuy.ca/api/v2/json/product/{PRODUCT_ID}?lang=en-CA"
PRODUCT_NAME = "MacBook Air 13\" M5 (Best Buy Canada)"
TARGET_PRICE = 1399.00   # alert if price drops below this

CONFIG_FILE = Path(__file__).parent / "config.json"
STATE_FILE  = Path(__file__).parent / "last_price.json"

# ── Load config ───────────────────────────────────────────────────────────────
def load_config():
    if not CONFIG_FILE.exists():
        print("ERROR: config.json not found. Run setup.py first.")
        raise SystemExit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)

# ── Fetch price ───────────────────────────────────────────────────────────────
def fetch_price():
    """Fetch price from Best Buy Canada product API."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Accept-Language": "en-CA,en;q=0.9",
        "Referer": "https://www.bestbuy.ca/",
    }
    req = urllib.request.Request(API_URL, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    # API returns salePrice or regularPrice
    price = data.get("salePrice") or data.get("regularPrice")
    if price is None:
        raise ValueError(f"Price not found in API response. Keys: {list(data.keys())}")
    return float(price)

# ── Mac notification ──────────────────────────────────────────────────────────
def send_mac_notification(title, message):
    script = f'display notification "{message}" with title "{title}" sound name "Ping"'
    subprocess.run(["osascript", "-e", script], check=False)

# ── Email ─────────────────────────────────────────────────────────────────────
def send_email(config, subject, body):
    gmail = config["gmail"]
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"]    = gmail["address"]
    msg["To"]      = gmail["address"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail["address"], gmail["app_password"])
        server.send_message(msg)

# ── State helpers ─────────────────────────────────────────────────────────────
def load_last_price():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f).get("price")
    return None

def save_last_price(price):
    with open(STATE_FILE, "w") as f:
        json.dump({"price": price}, f)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    config = load_config()

    print(f"Checking price for {PRODUCT_NAME}...")
    try:
        current_price = fetch_price()
    except Exception as e:
        print(f"Failed to fetch price: {e}")
        return

    last_price = load_last_price()
    print(f"Current price: ${current_price:,.2f} CAD | Last seen: ${last_price:,.2f} CAD" if last_price else f"Current price: ${current_price:,.2f} CAD (first run)")

    save_last_price(current_price)

    # Alert if price is below target AND lower than last seen price
    price_dropped = (last_price is not None and current_price < last_price)
    below_target  = current_price < TARGET_PRICE

    if below_target or price_dropped:
        drop_msg = ""
        if last_price:
            saved = last_price - current_price
            drop_msg = f" (dropped ${saved:,.2f} from ${last_price:,.2f})"

        title   = f"💸 MacBook Air price drop!"
        message = f"Now ${current_price:,.2f} CAD{drop_msg} on Best Buy Canada"
        url_msg = f"\n\n{PRODUCT_URL}"

        print(f"ALERT: {title} — {message}")
        send_mac_notification(title, message)

        try:
            send_email(
                config,
                subject=f"[Price Alert] {PRODUCT_NAME} — ${current_price:,.2f} CAD",
                body=f"{message}\n\nBuy it here:{url_msg}\n\nThis alert was triggered because the price dropped below ${TARGET_PRICE:,.2f} CAD."
            )
            print("Email sent.")
        except Exception as e:
            print(f"Email failed: {e}")
    else:
        print("No price drop detected. No alert sent.")

if __name__ == "__main__":
    main()
