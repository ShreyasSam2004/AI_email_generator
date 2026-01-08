# GitHub Actions Setup Guide

## Overview

GitHub Actions will run your AI News Aggregator automatically every day at 9 AM UTC (completely free!).

You need:
1. Free PostgreSQL database (Neon.tech recommended)
2. Add 8 secrets to GitHub

---

## Step 1: Create Free PostgreSQL Database

### Option A: Neon.tech (Recommended)

1. Go to https://neon.tech
2. Click "Sign Up" → Sign in with GitHub
3. Click "Create a project"
4. Give it a name: `ai-news-aggregator`
5. Select region closest to you
6. Click "Create Project"

7. **Copy Connection Details:**
   - On the dashboard, you'll see connection details
   - Note down these values:
     - Host (something like `ep-xxx.us-east-2.aws.neon.tech`)
     - Database name (usually `neondb`)
     - User (usually your username)
     - Password (click "Show password")
     - Port (always `5432`)

**Free Tier:** 3GB storage, 100 hours compute/month (more than enough!)

### Option B: Supabase

1. Go to https://supabase.com
2. Sign in with GitHub
3. Create new project
4. Go to Settings → Database
5. Copy connection details under "Connection string"

---

## Step 2: Add Secrets to GitHub

1. Go to your repository: https://github.com/ShreyasSam2004/AI_email_generator

2. Click **Settings** (top right of your repo)

3. In the left sidebar, click **Secrets and variables** → **Actions**

4. Click **New repository secret**

5. Add these **8 secrets** one by one:

   | Secret Name | Value | Where to Get |
   |------------|-------|--------------|
   | `OPENAI_API_KEY` | `sk-proj-...` | Your OpenAI API key |
   | `POSTGRES_HOST` | `ep-xxx.neon.tech` | From Neon dashboard |
   | `POSTGRES_DB` | `neondb` | From Neon dashboard (database name) |
   | `POSTGRES_USER` | Your username | From Neon dashboard |
   | `POSTGRES_PASSWORD` | Your password | From Neon dashboard (click "Show password") |
   | `POSTGRES_PORT` | `5432` | Always 5432 for PostgreSQL |
   | `MY_EMAIL` | `your@gmail.com` | Your Gmail address |
   | `APP_PASSWORD` | `xxxx xxxx xxxx xxxx` | Your Gmail app password |

6. For each secret:
   - Click "New repository secret"
   - Enter the **Name** (exactly as shown above)
   - Paste the **Value**
   - Click "Add secret"

---

## Step 3: Test the Workflow

1. Go to your repo: https://github.com/ShreyasSam2004/AI_email_generator

2. Click the **Actions** tab

3. You should see "Daily AI News Digest" workflow

4. Click on it

5. Click **Run workflow** button (on the right side)

6. Click the green **Run workflow** button in the popup

7. Wait 2-3 minutes for it to complete

8. **Check your email!** You should receive the AI news digest

9. If it fails:
   - Click on the failed run
   - Expand the failed step to see error logs
   - Common issues:
     - Wrong secret values
     - Database connection issues

---

## Step 4: It's Now Automated!

That's it! Your workflow will now run automatically **every day at 9 AM UTC**.

### Change the Schedule

Edit `.github/workflows/daily-digest.yml` and change the cron line:

```yaml
schedule:
  - cron: '0 9 * * *'  # minute hour day month day-of-week
```

**Examples:**
- `0 0 * * *` - Midnight UTC
- `0 17 * * *` - 5 PM UTC
- `30 3 * * *` - 3:30 AM UTC (9 AM IST)
- `0 9 * * 1` - 9 AM UTC every Monday only

### Convert UTC to Your Timezone

- **EST**: UTC - 5 hours
- **PST**: UTC - 8 hours
- **IST**: UTC + 5:30 hours
- **GMT**: Same as UTC

Example: For 9 AM IST, use 3:30 AM UTC = `30 3 * * *`

---

## Monitoring

### View Run History

1. Go to **Actions** tab
2. See all past runs with status (success/fail)
3. Click any run to see detailed logs

### Email Notifications

GitHub will email you if a workflow fails (optional, can disable in settings)

---

## Troubleshooting

### Workflow fails with "Database connection error"

- Check your database secrets are correct
- Make sure Neon project is running (check Neon dashboard)
- Verify `POSTGRES_HOST` doesn't include `postgresql://` prefix

### No email received

- Check workflow logs - did it run successfully?
- Verify `MY_EMAIL` and `APP_PASSWORD` are correct
- Check spam folder
- Make sure Gmail app password is still valid

### "No digests found" error

- First run might not have articles if sources didn't publish in last 24 hours
- Try running with manual trigger to test
- Check if scrapers are working (view logs)

---

## Cost

**Total: $0/month**

- GitHub Actions: 2,000 minutes/month free (you'll use ~30 minutes/month)
- Neon database: Free tier (3GB storage, 100 hours/month)

---

## Next Steps

Once you confirm it's working:
1. Star your own repo to remember it
2. Check Actions tab daily to monitor runs
3. Enjoy your automated AI news digests!
