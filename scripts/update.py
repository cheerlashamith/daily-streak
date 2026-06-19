#!/usr/bin/env python3
"""
Daily GitHub Streak Agent
-------------------------
This script makes MULTIPLE real, meaningful changes every day so your GitHub
contribution graph stays green with 7 commits per day. Each run appends a
unique entry to logs/activity.md with a different quote and run number.

It is designed to run inside GitHub Actions (free), but you can also run
it locally:  python scripts/update.py
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path
import json
import hashlib

# ---- Config -----------------------------------------------------------------
# Change this to your timezone offset (hours) so the date matches YOUR day.
# Example: India (IST) = +5.5, UTC = 0, US Eastern (EST) = -5
TZ_OFFSET_HOURS = 5.5

COMMITS_PER_DAY = 7

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "logs" / "activity.md"
STATE_FILE = ROOT / "logs" / "state.json"

# 35 quotes — 5 per slot, so each of the 7 daily commits always has fresh
# content even across consecutive days.
QUOTES = [
    # Slot 1 — Early Morning (06:00 IST)
    "Rise and code — the early commit catches the streak.",
    "The sunrise doesn't wait, and neither does your streak.",
    "First light, first commit.",
    "A fresh day, a fresh push.",
    "Coffee loaded. Streak updated.",

    # Slot 2 — Morning (08:30 IST)
    "Morning momentum builds winning habits.",
    "Consistency beats intensity.",
    "Small daily improvements lead to stunning results.",
    "The secret of getting ahead is getting started.",
    "Good morning, green square.",

    # Slot 3 — Late Morning (11:00 IST)
    "Halfway through the morning, still shipping.",
    "Done is better than perfect.",
    "A year from now you'll wish you had started today.",
    "Discipline is choosing what you want most over what you want now.",
    "Keep the chain going.",

    # Slot 4 — Afternoon (01:30 IST)
    "Afternoon push — the streak keeps rolling.",
    "Showing up is half the battle.",
    "Progress, not perfection.",
    "Code a little, learn a little, grow a lot.",
    "Lunchtime commit. Productivity never stops.",

    # Slot 5 — Evening (04:00 IST)
    "Evening energy. Ship it.",
    "Tiny steps, every day, become a giant leap.",
    "The best time to plant a tree was yesterday. The next best is now.",
    "Your future self will thank you for this commit.",
    "Pushing through the afternoon slump.",

    # Slot 6 — Late Evening (06:30 IST)
    "Golden hour commit — still going strong.",
    "Six commits deep. Unstoppable.",
    "Persistence turns beginners into experts.",
    "Day isn't over until the code says so.",
    "Almost there — keep the streak alive.",

    # Slot 7 — Night (09:00 IST)
    "Final push of the day. Streak secured. 🔒",
    "Seven commits today. Legend status unlocked.",
    "Goodnight, GitHub. See you tomorrow.",
    "Today's work becomes tomorrow's foundation.",
    "Streak complete. Rest well, coder.",
]


def now_local():
    tz = timezone(timedelta(hours=TZ_OFFSET_HOURS))
    return datetime.now(tz)


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"streak": 0, "last_date": None, "total_runs": 0, "daily_commit_number": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def pick_quote(day_of_year: int, commit_number: int) -> str:
    """Pick a unique quote based on day of year and which commit this is (1-7).
    Each commit slot (1-7) has 5 dedicated quotes. We rotate through them
    using day_of_year so content changes every day."""
    slot_index = (commit_number - 1) % COMMITS_PER_DAY      # 0-6
    quotes_per_slot = 5
    base = slot_index * quotes_per_slot                      # start of slot's quotes
    offset = day_of_year % quotes_per_slot                   # rotate daily
    return QUOTES[base + offset]


def main():
    dt = now_local()
    today = dt.strftime("%Y-%m-%d")
    stamp = dt.strftime("%Y-%m-%d %H:%M:%S UTC%z")
    # Format timezone like UTC+05:30
    tz_str = stamp[-5:]  # e.g. +0530
    stamp = stamp[:-5] + tz_str[:3] + ":" + tz_str[3:]  # +05:30
    day_of_year = int(dt.strftime("%j"))

    state = load_state()

    # ── Streak logic ────────────────────────────────────────────
    if state.get("last_date") == today:
        # Same day — increment daily commit number
        state["daily_commit_number"] = state.get("daily_commit_number", 0) + 1
    else:
        # New day
        yesterday = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
        if state.get("last_date") == yesterday:
            state["streak"] = state.get("streak", 0) + 1
        elif state.get("last_date") is None:
            state["streak"] = 1
        else:
            state["streak"] = 1
        state["last_date"] = today
        state["daily_commit_number"] = 1   # first commit of the day

    commit_num = state["daily_commit_number"]
    state["total_runs"] = state.get("total_runs", 0) + 1

    quote = pick_quote(day_of_year, commit_num)

    # ── Ensure header exists ────────────────────────────────────
    if not LOG_FILE.exists():
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOG_FILE.write_text(
            "# 🟢 Daily Activity Log\n\n"
            "Automatically maintained by the Daily Streak Agent.\n\n"
            "| Date | Time | Streak | Commit # | Quote |\n"
            "|------|------|--------|----------|-------|\n",
            encoding="utf-8"
        )

    line = (
        f"| {today} | {stamp} | "
        f"\U0001f525 {state['streak']} | "
        f"{commit_num}/{COMMITS_PER_DAY} | {quote} |\n"
    )
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

    save_state(state)

    print(f"[OK] Logged {today} -- commit {commit_num}/{COMMITS_PER_DAY}")
    print(f"     Streak : {state['streak']} day(s)")
    print(f"     Total  : {state['total_runs']} runs")
    print(f"     Quote  : {quote}")


if __name__ == "__main__":
    main()
