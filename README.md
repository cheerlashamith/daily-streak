# Daily GitHub Streak Agent

An agent that automatically commits to your GitHub repo **once a day**, so your
contribution graph stays green. It runs in **GitHub Actions** (free cloud) —
your PC does **not** need to be on.

![architecture](diagrams/architecture.png)

<p align="center">
  <img src="diagrams/made-by-cherla-shamith.svg" alt="Made by Cherla Shamith" width="640"/>
</p>

---

## What it does

Every day, a script adds today's date + a short quote to `logs/activity.md`,
then commits and pushes it. That commit = one green square on your graph.

---

## How it works (step by step)

Every day, this happens automatically — even if your laptop is off:

```
⏰ 1. The timer (YAML cron) fires at the set time
        │
        ▼
💻 2. GitHub rents a free Linux computer
        │
        ▼
📥 3. It downloads your repo onto that computer
        │
        ▼
🐍 4. It runs update.py  →  adds a new line to activity.md
        │
        ▼
💾 5. git commit + git push  →  the change goes to your repo
        │
        ▼
🟢 6. New commit = one green square on your graph
        │
        ▼
🗑️ 7. The rented computer is thrown away (until tomorrow)
```

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

**4. Make commits count for you** (important)
In `.github/workflows/daily-commit.yml`, replace these lines with your info
(get your email from GitHub → Settings → Emails):
```yaml
git config user.name  "YOUR_GITHUB_USERNAME"
git config user.email "12345678+YOUR_GITHUB_USERNAME@users.noreply.github.com"
```

**5. Test it**
Repo → **Actions** tab → **Daily Streak Commit** → **Run workflow**.
Check your repo for a new commit. From now on it runs by itself.

---

## Change the time

In `daily-commit-agent.yml`, edit the cron line (time is in **UTC**):
```yaml
- cron: "30 21 * * *"   # 21:30 UTC = 03:00 IST
```
Use https://crontab.guru to set your own time.

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
- **Timing:** GitHub may run the job a few minutes late. That's normal.
- **Graph stays grey?** You skipped step 4 (email must be your GitHub email).
- **Push error?** You skipped step 3 (read & write permissions).
- **Runs by itself:** Once set up, you never have to do anything again.

---

<p align="center">
  <img src="diagrams/made-by-cherla-shamith.svg" alt="Made by Cherla Shamith" width="500"/>
</p>

<p align="center"><b>© Cherla Shamith</b> · Daily GitHub Streak Agent</p>

---

## Files

```
.github/workflows/daily-commit.yml   automation + schedule
scripts/update.py                    the daily script
logs/                                generated log
diagrams/                            architecture image
README.md
```
