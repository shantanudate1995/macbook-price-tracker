#!/usr/bin/env python3
"""
Daily summary emailer for MacBook Air Price Tracker.
Sends an end-of-day email confirming the price hasn't changed.
Scheduled via launchd to run once per day at 8pm.
"""

import json
import smtplib
from datetime import date
from email.mime.text import MIMEText
from pathlib import Path

PRODUCT_URL  = "https://www.bestbuy.ca/en-ca/product/apple-macbook-air-13-6-w-touch-id-2026-midnight-apple-m5-16gb-ram-512gb-ssd-english/19791103"
PRODUCT_NAME = 'MacBook Air 13" M5 (Best Buy Canada)'
TARGET_PRICE = 1499.00

CONFIG_FILE = Path(__file__).parent / "config.json"
STATE_FILE  = Path(__file__).parent / "last_price.json"

def load_config():
    if not CONFIG_FILE.exists():
        print("ERROR: config.json not found. Run setup.py first.")
        raise SystemExit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_last_price():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f).get("price")
    return None

def send_email(config, subject, body):
    gmail = config["gmail"]
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"]    = gmail["address"]
    msg["To"]      = gmail["address"]
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail["address"], gmail["app_password"])
        server.send_message(msg)

def main():
    config      = load_config()
    last_price  = load_last_price()
    today       = date.today().strftime("%B %d, %Y")

    if last_price is None:
        print("No price data yet — skipping daily summary.")
        return

    still_needed = last_price - TARGET_PRICE
    subject = f"[Daily Update] MacBook Air still ${last_price:,.2f} CAD — {today}"
    body = f"""Daily Price Tracker Update — {today}

Product : {PRODUCT_NAME}
Price today : ${last_price:,.2f} CAD
Your target : below ${TARGET_PRICE:,.2f} CAD
Still needs to drop : ${still_needed:,.2f} CAD

No price change was detected today. The tracker is running and will email you immediately if the price drops.

View on Best Buy Canada:
{PRODUCT_URL}
"""

    print(f"Sending daily summary for {today}...")
    try:
        send_email(config, subject, body)
        print("Daily summary sent.")
    except Exception as e:
        print(f"Email failed: {e}")

if __name__ == "__main__":
    main()
