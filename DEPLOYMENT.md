# Deployment Guide - AI News Aggregator

This guide shows you how to deploy your AI News Aggregator to run automatically every 24 hours.

## Option 1: Railway.app (Recommended - Easiest)

**Pros:**
- Free PostgreSQL database included
- Built-in cron scheduling
- Easy GitHub integration
- No server management

**Free Tier Limits:**
- $5 credit/month (enough for daily runs)
- 500 hours execution time

### Setup Steps:

1. **Sign up for Railway**
   - Go to https://railway.app
   - Click "Login" and sign in with GitHub
   - Authorize Railway to access your repositories

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `ShreyasSam2004/AI_email_generator`
   - Railway will detect Python and auto-deploy

3. **Add PostgreSQL Database**
   - In your project, click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway automatically provisions it
   - It will auto-inject `DATABASE_URL` variable

4. **Update Database Connection Code**
   - You'll need to modify `app/database/connection.py` to use Railway's `DATABASE_URL`
   - Railway provides it in format: `postgresql://user:pass@host:port/db`

5. **Set Environment Variables**
   - Click on your service → "Variables" tab
   - Add these secrets:
     ```
     OPENAI_API_KEY=your_openai_api_key
     MY_EMAIL=your_email@gmail.com
     APP_PASSWORD=your_gmail_app_password
     ```

6. **Configure Cron Schedule**
   - The `railway.toml` file is already set up
   - It runs daily at 9 AM UTC
   - Edit the schedule line to change time:
     ```toml
     schedule = "0 9 * * *"  # 9 AM UTC daily
     ```
   - Cron format: `minute hour day month day-of-week`

7. **Deploy**
   - Push changes to GitHub (cron config)
   - Railway auto-deploys from GitHub
   - Check logs to verify it works

---

## Option 2: GitHub Actions (Free, Requires External Database)

**Pros:**
- Completely free
- Runs on GitHub's infrastructure
- No account signup needed (you already have GitHub)

**Cons:**
- Need to host PostgreSQL externally (Railway, Neon, Supabase)

### Setup Steps:

1. **Set Up External PostgreSQL Database**

   Choose one of these free database hosts:

   **Option A: Neon.tech (Recommended)**
   - Go to https://neon.tech
   - Sign up with GitHub
   - Create new project
   - Copy connection string

   **Option B: Supabase**
   - Go to https://supabase.com
   - Sign up with GitHub
   - Create new project
   - Go to Settings → Database → Connection string

   **Option C: Railway (just database)**
   - Follow Railway setup above but only create database
   - Get connection details from Railway dashboard

2. **Add Secrets to GitHub Repository**
   - Go to your repo: https://github.com/ShreyasSam2004/AI_email_generator
   - Click "Settings" → "Secrets and variables" → "Actions"
   - Click "New repository secret"
   - Add each secret:
     ```
     OPENAI_API_KEY=your_key_here
     POSTGRES_USER=your_db_user
     POSTGRES_PASSWORD=your_db_password
     POSTGRES_DB=your_db_name
     POSTGRES_HOST=your_db_host
     POSTGRES_PORT=5432
     MY_EMAIL=your_email@gmail.com
     APP_PASSWORD=your_gmail_app_password
     ```

3. **GitHub Actions is Already Configured**
   - The workflow file `.github/workflows/daily-digest.yml` is ready
   - It runs daily at 9 AM UTC
   - To change schedule, edit the cron line:
     ```yaml
     schedule:
       - cron: '0 9 * * *'  # minute hour day month day-of-week
     ```

4. **Test the Workflow**
   - Go to "Actions" tab in your GitHub repo
   - Select "Daily AI News Digest"
   - Click "Run workflow" → "Run workflow"
   - Watch it execute live
   - Check your email for the digest

5. **Automated Daily Runs**
   - GitHub Actions will now run automatically daily
   - View history in the "Actions" tab
   - Get email notifications if workflow fails

---

## Option 3: AWS Lambda + EventBridge (Advanced)

**Pros:**
- Highly scalable
- Pay only for execution time (very cheap)

**Cons:**
- More complex setup
- Requires AWS account
- Need to manage dependencies

I can help set this up if you prefer AWS.

---

## Option 4: Heroku (Simple but Paid)

**Note:** Heroku no longer has a free tier, minimum $5/month

**Pros:**
- Very easy to deploy
- Includes PostgreSQL addon

**Cons:**
- Costs money ($5-7/month)

---

## Recommended Approach for You

I recommend **GitHub Actions** + **Neon.tech** database:

1. **Why GitHub Actions?**
   - Completely free
   - You already have GitHub
   - No new platform to learn
   - Easy to monitor in your repo

2. **Why Neon.tech database?**
   - Generous free tier (3GB storage)
   - PostgreSQL compatible
   - Auto-scales to zero (no cost when idle)
   - Easy setup

3. **Total Cost:** $0/month

---

## Updating the Schedule

All options use cron syntax:

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-6, Sunday=0)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

**Examples:**
- `0 9 * * *` - 9 AM UTC daily
- `0 0 * * *` - Midnight UTC daily
- `0 17 * * *` - 5 PM UTC daily
- `0 9 * * 1` - 9 AM UTC every Monday
- `0 9 1,15 * *` - 9 AM on 1st and 15th of each month

**Convert to Your Timezone:**
- UTC to EST: subtract 5 hours
- UTC to PST: subtract 8 hours
- UTC to IST: add 5.5 hours

Example: For 9 AM IST, use 3:30 AM UTC = `30 3 * * *`

---

## Next Steps

Choose your deployment method and let me know if you need help with any specific step!
