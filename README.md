# Daily GitHub Streak Agent

An agent that automatically commits to your GitHub repo **once a day**, so your
contribution graph stays green. It runs in **GitHub Actions** (free cloud) —
your PC does **not** need to be on.

![architecture](diagrams/architecture.png)

---

## What it does

Every day, a script adds today's date + a short quote to `logs/activity.md`,
then commits and pushes it. That commit = one green square on your graph.

---

## How it works

1. **GitHub Actions** runs the job once a day (on a timer).
2. It starts a free Linux machine and runs `scripts/update.py`.
3. The script writes a new line into `logs/activity.md`.
4. The job commits and pushes that change to your repo.

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

## Notes

- **Free:** Public repos get unlimited Actions minutes. No Pro plan needed.
- **Timing:** GitHub may run the job a few minutes late. That's normal.
- **Graph stays grey?** You skipped step 4 (email must be your GitHub email).
- **Push error?** You skipped step 3 (read & write permissions).

---

## Files

```
.github/workflows/daily-commit.yml   automation + schedule
scripts/update.py                    the daily script
logs/                                generated log
diagrams/                            architecture image
README.md
```
