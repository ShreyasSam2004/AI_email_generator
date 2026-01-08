# New AI News Sources Added

## Summary

I've added **3 new high-frequency AI news sources** to your aggregator to ensure you get more daily content:

1. **VentureBeat AI** - Multiple articles per week on enterprise AI
2. **TechCrunch AI** - Multiple articles per day (very active!)
3. **ScienceDaily AI** - Research-focused AI news, multiple per week

## What Was Changed

### New Files Created

1. **Scrapers** (following your existing pattern):
   - `app/scrapers/venturebeat.py` - VentureBeat AI RSS scraper
   - `app/scrapers/techcrunch.py` - TechCrunch AI RSS scraper
   - `app/scrapers/sciencedaily.py` - ScienceDaily AI RSS scraper

2. **Migration Script**:
   - `create_new_tables.py` - Creates the 3 new database tables

### Files Modified

1. **Database Models** (`app/database/models.py`):
   - Added `VentureBeatArticle` model
   - Added `TechCrunchArticle` model
   - Added `ScienceDailyArticle` model

2. **Repository** (`app/database/repository.py`):
   - Added `bulk_create_venturebeat_articles()`
   - Added `bulk_create_techcrunch_articles()`
   - Added `bulk_create_sciencedaily_articles()`
   - Updated `get_articles_without_digest()` to include all 3 new sources

3. **Runner** (`app/runner.py`):
   - Imports all 3 new scrapers
   - Instantiates them in `run_scrapers()`
   - Scrapes articles from all 3 sources
   - Saves them to database
   - Returns counts in results

4. **Main** (`main.py`):
   - Updated to display counts for all 3 new sources

## How to Use

### Step 1: Create the New Database Tables

Run the migration script once:

```bash
python create_new_tables.py
```

This will create the 3 new tables in your PostgreSQL database.

### Step 2: Run Your Scraper

Now run your main script as usual:

```bash
python main.py
```

This will scrape from all sources:
- YouTube (Matthew Berman's channel)
- OpenAI official blog
- Anthropic (3 feeds)
- **VentureBeat AI** ✨ NEW
- **TechCrunch AI** ✨ NEW
- **ScienceDaily AI** ✨ NEW

### Step 3: Process Digests

The digest generation already includes the new sources automatically:

```bash
python -m app.services.process_digest
```

### Step 4: Send Email

The email pipeline will include articles from all sources:

```bash
python -m app.services.process_email
```

## Expected Results

With these new sources, you should now see:

- **TechCrunch**: 3-10+ articles per day (very high volume!)
- **VentureBeat**: 2-5 articles per week
- **ScienceDaily**: 2-4 research articles per week

Combined with YouTube, you should have **daily content** for your email digests instead of getting sparse emails when OpenAI/Anthropic don't publish.

## RSS Feed URLs Used

- VentureBeat AI: `https://venturebeat.com/category/ai/feed/`
- TechCrunch AI: `https://techcrunch.com/category/artificial-intelligence/feed/`
- ScienceDaily AI: `https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml`

## Testing Individual Scrapers

You can test each scraper individually:

```bash
# Test VentureBeat scraper
python -m app.scrapers.venturebeat

# Test TechCrunch scraper
python -m app.scrapers.techcrunch

# Test ScienceDaily scraper
python -m app.scrapers.sciencedaily
```

## Notes

- All scrapers follow your existing pattern (RSS feed parsing with time filtering)
- No markdown conversion needed (uses description field like OpenAI)
- Fully integrated into your digest generation pipeline
- Each source has its own database table to avoid conflicts
- Supports duplicate detection (won't re-scrape existing articles)

---

**Ready to go!** Just run the migration script once, then use your existing workflow.
