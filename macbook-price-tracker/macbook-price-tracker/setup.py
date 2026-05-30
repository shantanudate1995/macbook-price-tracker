#!/usr/bin/env python3
"""
Setup wizard for MacBook Air Price Tracker.
Run this once to configure your Gmail credentials.
"""

import json
import smtplib
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

def main():
    print("\n┌─────────────────────────────────────────┐")
    print("│  MacBook Air Price Tracker — Setup      │")
    print("└─────────────────────────────────────────┘\n")

    print("You'll need a Gmail App Password (not your regular password).")
    print("Get one at: https://myaccount.google.com/apppasswords\n")

    email = input("Your Gmail address: ").strip()
    app_password = input("Gmail App Password (16 chars, no spaces): ").strip().replace(" ", "")

    print("\nTesting connection to Gmail...")
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, app_password)
        print("✓ Gmail login successful!\n")
    except Exception as e:
        print(f"✗ Gmail login failed: {e}")
        print("Double-check your app password and try again.")
        raise SystemExit(1)

    config = {
        "gmail": {
            "address": email,
            "app_password": app_password
        }
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

    print(f"✓ Config saved to {CONFIG_FILE}")
    print("\nNext step: run install_launchd.sh to start the hourly background checker.")
    print("Or test it right now with:  python3 check_price.py\n")

if __name__ == "__main__":
    main()
