# MacBook Air Price Tracker

I'm a product manager transitioning into AI PM roles. One of the first things 
I noticed when I started learning to build was that the most useful projects 
solve a problem you actually have. I wanted a MacBook Air M5 but didn't want 
to watch the Best Buy Canada page manually every day. So I automated it.

This is my first Python project. No AI involved — just automation, APIs, and 
a background service that runs silently on my Mac. I built it to develop the 
muscle of turning a personal problem into working software.

---

## What it does

Monitors the MacBook Air 13" M5 on Best Buy Canada every hour. If the price 
drops below $1,499 CAD or falls from its last seen price, it sends a Mac 
desktop notification and a Gmail alert with the current price and a direct 
link to buy.

Runs silently in the background via macOS `launchd`. Survives reboots. 
Never misses a price check.

---

## How it works

- Calls the Best Buy Canada product API directly — no scraping, no browser
- Stores the last seen price in `last_price.json` to detect drops between runs
- Sends a Mac notification via AppleScript and an email via Gmail SMTP
- Scheduled hourly via macOS `launchd` — a native Mac background job system

---

## What I learned building this

**APIs are more reliable than scraping — but you have to find them.**

Best Buy's public website would have been painful to scrape — dynamic content, 
anti-bot protection, changing DOM structure. Finding the underlying JSON API 
(`/api/v2/json/product/{id}`) made the whole thing simpler and more reliable. 
Lesson: before scraping a page, check if there's an API behind it.

**State management matters even in simple scripts.**

The script needs to know the last seen price to detect a drop. That means 
persisting state between hourly runs. I used a simple JSON file 
(`last_price.json`) for this. It's not sophisticated but it works and it 
taught me the core problem that databases solve — you need somewhere to 
remember things between executions.

**Background jobs on Mac are unintuitive.**

macOS uses `launchd` for background jobs instead of the more common `cron`. 
The `.plist` XML format is verbose and the error messages when it fails are 
cryptic. Getting the job to survive reboots and log errors properly took 
longer than the actual Python code. Infrastructure is always harder than 
the feature.

**The hardest part was Gmail authentication.**

Gmail no longer accepts regular passwords for SMTP. You need an App Password 
from Google's security settings — a separate 16-character credential that 
only works for this purpose. This is a small taste of OAuth and credential 
management complexity that shows up in every real product that sends email.

---

## What this project doesn't do that a real product would

This tracker is hardcoded to one product on one retailer. A real version 
would track multiple products, support multiple retailers, let users set 
their own price targets, and store history to show price trends over time. 
The gap between a personal script and a shippable product is mostly about 
configuration, reliability, and handling cases you didn't think of when 
you wrote it for yourself.

---

## Setup

**1. Get a Gmail App Password**

Go to myaccount.google.com/apppasswords, create one named "Price Tracker", 
and copy the 16-character password.

**2. Run setup**

```bash
cd ~/macbook-price-tracker
python3 setup.py
```

Enter your Gmail address and app password when prompted.

**3. Install the background job**

```bash
bash install_launchd.sh
```

The tracker now runs every hour in the background and survives reboots.

**Test it manually:**

```bash
python3 check_price.py
```

**View logs:**

```bash
tail -f ~/macbook-price-tracker/price_tracker.log
```

**Stop it:**

```bash
launchctl unload ~/Library/LaunchAgents/com.user.macbook-price-tracker.plist
```

---

## Files

| File | Purpose |
|---|---|
| `check_price.py` | Main script — fetches price, compares, sends alerts |
| `setup.py` | One-time config wizard — stores Gmail credentials |
| `install_launchd.sh` | Installs the hourly background job via launchd |
| `daily_summary.py` | Optional daily digest email with price history |
| `config.json` | Gmail credentials (created by setup.py, gitignored) |
| `last_price.json` | Last seen price — persists state between runs |
| `price_tracker.log` | Output log for debugging |

---

## Built with

- Python 3.14 (standard library only — no dependencies)
- Best Buy Canada product API
- Gmail SMTP with App Password authentication
- macOS launchd for background scheduling
- AppleScript for Mac desktop notifications