# Daily GitHub Streak Agent

An automated agent that commits to your GitHub repo **7 times a day**, keeping
your contribution graph **deeply green**. It runs entirely in **GitHub Actions**
(free cloud) — your PC does **not** need to be on.

![architecture](diagrams/architecture.png)

<p align="center">
  <img src="diagrams/made-by-cherla-shamith.svg" alt="Made by Cherla Shamith" width="640"/>
</p>

---

## What it does

Seven times a day, the agent runs `scripts/update.py` which:
1. Appends a **unique entry** (date, time, streak, commit number, quote) to `logs/activity.md`
2. Updates the streak counter in `logs/state.json`
3. Commits and pushes — each commit = one **green square** on your contribution graph

Each run uses a **different motivational quote** (35 total — 5 per time slot),
so every commit has genuinely unique content.

---

## Daily Schedule (7 commits/day)

All times are automatically handled by GitHub Actions cron (UTC), shown below
in **IST (UTC+05:30)** for India / Andhra Pradesh:

| # | UTC Time | IST Time | Description |
|---|----------|----------|-------------|
| 1 | 00:30 | 06:00 AM | ☀️ Early morning |
| 2 | 03:00 | 08:30 AM | 🌅 Morning |
| 3 | 05:30 | 11:00 AM | 📖 Late morning |
| 4 | 08:00 | 01:30 PM | 🍽️ Afternoon |
| 5 | 10:30 | 04:00 PM | 🌤️ Evening |
| 6 | 13:00 | 06:30 PM | 🌇 Late evening |
| 7 | 15:30 | 09:00 PM | 🌙 Night |

> **Why spread across the day?** GitHub Actions may skip or delay cron jobs that
> are too close together. A 2–3 hour gap between each run ensures maximum
> reliability. It also makes the contribution graph look more natural.

---

## How it works (step by step)

Every run (7× per day), this happens automatically — even if your laptop is off:

```
⏰ 1. The cron timer fires at the scheduled time
        │
        ▼
💻 2. GitHub spins up a free Linux VM
        │
        ▼
📥 3. It checks out your repo
        │
        ▼
🐍 4. It runs update.py  →  appends a unique entry to activity.md
        │                     (date + time + streak + commit #/7 + quote)
        ▼
💾 5. git commit + git push  →  the change goes to your repo
        │
        ▼
🟢 6. New commit = one green square on your graph
        │
        ▼
🗑️ 7. The VM is destroyed (until the next scheduled run)
```

This repeats **7 times a day**, giving you **7 green contributions daily**.
No PC, no server, no payment needed.

---

## Setup (one time)

**1. Create a repo**
Go to https://github.com/new → make it **Public** → Create.

**2. Add the files**
Upload these to the repo (keep the folders):
- `.github/workflows/daily-commit.yml`
- `scripts/update.py`
- `logs/.gitkeep`
- `README.md`

**3. Allow it to commit**
Repo → **Settings → Actions → General → Workflow permissions** →
choose **Read and write permissions** → Save.

**4. Make commits count for YOU** (important!)
In `.github/workflows/daily-commit.yml`, replace these lines with your info
(find your email at GitHub → Settings → Emails):
```yaml
git config user.name  "YOUR_GITHUB_USERNAME"
git config user.email "YOUR_GITHUB_EMAIL"
```

**5. Test it**
Repo → **Actions** tab → **Daily Streak Commit** → **Run workflow**.
Check your repo for a new commit. From now on it runs 7× a day by itself.

---

## Change the schedule

In `.github/workflows/daily-commit.yml`, edit the cron lines (times in **UTC**):
```yaml
on:
  schedule:
    - cron: "30 0 * * *"    # 06:00 AM IST
    - cron: "0 3 * * *"     # 08:30 AM IST
    - cron: "30 5 * * *"    # 11:00 AM IST
    - cron: "0 8 * * *"     # 01:30 PM IST
    - cron: "30 10 * * *"   # 04:00 PM IST
    - cron: "0 13 * * *"    # 06:30 PM IST
    - cron: "30 15 * * *"   # 09:00 PM IST
```
Use https://crontab.guru to set your own times.

> **Tip:** Keep at least a **2-hour gap** between runs. GitHub Actions cron is
> best-effort and may delay or skip tightly-spaced schedules.

---

## Do I need a Linux computer? (I use Windows)

**No.** Your own computer's operating system does not matter at all.

- The agent runs on **GitHub's** computers, not yours.
- GitHub uses a Linux machine *in the cloud* (the `ubuntu-latest` line) — that
  is GitHub's machine, set up automatically. You never touch it.
- You only use the **GitHub website** in your browser, which works the same on
  Windows, Mac, or anything.
- Your laptop can be **off** — the job still runs. Nothing is installed on your
  Windows PC, nothing is disturbed.

So Windows is totally fine. ✅

---

## Notes

- **Free:** Public repos get unlimited Actions minutes. No Pro plan needed.
- **7 commits/day:** The agent makes 7 commits daily with unique content.
- **Timing:** GitHub may run jobs up to 15 minutes late. That's normal.
- **Graph stays grey?** Make sure your git email matches your GitHub account email (step 4).
- **Push error?** Check read & write permissions (step 3).
- **Fully automatic:** Once set up, you never have to do anything again.

---

<p align="center">
  <img src="diagrams/made-by-cherla-shamith.svg" alt="Made by Cherla Shamith" width="500"/>
</p>

<p align="center"><b>© Cherla Shamith</b> · Daily GitHub Streak Agent</p>

---

## Files

```
.github/workflows/daily-commit.yml   automation + 7× daily schedule
scripts/update.py                    the daily script (35 rotating quotes)
logs/activity.md                     auto-generated activity log
logs/state.json                      streak & run counter state
diagrams/                            architecture image
README.md                            this file
```
