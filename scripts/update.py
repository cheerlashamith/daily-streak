#!/usr/bin/env python3
"""
Daily GitHub Streak Agent
-------------------------
This script makes ONE real, meaningful change every day so your GitHub
contribution graph stays green. It appends today's date + a rotating
"daily quote" to logs/activity.md and bumps a streak counter.

It is designed to run inside GitHub Actions (free), but you can also run
it locally:  python scripts/update.py
"""

from datetime import datetime, timezone, timedelta
from pathlib import Path
import json

# ---- Config -----------------------------------------------------------------
# Change this to your timezone offset (hours) so the date matches YOUR day.
# Example: India (IST) = +5.5, UTC = 0, US Eastern (EST) = -5
TZ_OFFSET_HOURS = 5.5

ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = ROOT / "logs" / "activity.md"
STATE_FILE = ROOT / "logs" / "state.json"

# A small bank of quotes — one is picked based on the day number so the
# committed content actually changes and is a tiny bit interesting.
QUOTES = [
    "Consistency beats intensity.",
    "Small daily improvements lead to stunning results.",
    "A year from now you'll wish you had started today.",
    "The secret of getting ahead is getting started.",
    "Discipline is choosing what you want most over what you want now.",
    "Done is better than perfect.",
    "Showing up is half the battle.",
    "Tiny steps, every day, become a giant leap.",
    "Progress, not perfection.",
    "Code a little, learn a little, grow a lot.",
]


def now_local():
    tz = timezone(timedelta(hours=TZ_OFFSET_HOURS))
    return datetime.now(tz)


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"streak": 0, "last_date": None, "total_runs": 0}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def main():
    dt = now_local()
    today = dt.strftime("%Y-%m-%d")
    stamp = dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    day_of_year = int(dt.strftime("%j"))
    quote = QUOTES[day_of_year % len(QUOTES)]

    state = load_state()

    # Update streak logic
    if state.get("last_date") == today:
        # already ran today; still ensure a change so the commit is non-empty
        pass
    else:
        yesterday = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
        if state.get("last_date") == yesterday:
            state["streak"] = state.get("streak", 0) + 1
        else:
            state["streak"] = 1
        state["last_date"] = today

    state["total_runs"] = state.get("total_runs", 0) + 1

    # Ensure header exists
    if not LOG_FILE.exists():
        LOG_FILE.write_text(
            "# 🟢 Daily Activity Log\n\n"
            "Automatically maintained by the Daily Streak Agent.\n\n"
            "| Date | Time | Streak | Quote |\n"
            "|------|------|--------|-------|\n"
        )

    line = f"| {today} | {stamp} | 🔥 {state['streak']} | {quote} |\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

    save_state(state)

    print(f"✅ Logged {today}  (streak: {state['streak']}, total runs: {state['total_runs']})")
    print(f"   Quote: {quote}")


if __name__ == "__main__":
    main()
