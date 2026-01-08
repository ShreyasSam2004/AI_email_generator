from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel


class ScienceDailyArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class ScienceDailyScraper:
    def __init__(self):
        self.rss_url = "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml"

    def get_articles(self, hours: int = 24) -> List[ScienceDailyArticle]:
        feed = feedparser.parse(self.rss_url)
        if not feed.entries:
            return []

        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=hours)
        articles = []

        for entry in feed.entries:
            published_parsed = getattr(entry, "published_parsed", None)
            if not published_parsed:
                continue

            published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)

            # Fix: If the published time is in the future, it's a parsing bug
            if published_time > now:
                published_time = published_time.replace(year=published_time.year - 1)

            if published_time >= cutoff_time:
                articles.append(ScienceDailyArticle(
                    title=entry.get("title", ""),
                    description=entry.get("description", ""),
                    url=entry.get("link", ""),
                    guid=entry.get("id", entry.get("link", "")),
                    published_at=published_time,
                    category=entry.get("tags", [{}])[0].get("term") if entry.get("tags") else None
                ))

        return articles


if __name__ == "__main__":
    scraper = ScienceDailyScraper()

    # Debug: Check what's in the feed
    print("Debugging RSS feed:")
    feed = feedparser.parse(scraper.rss_url)
    print(f"Total entries: {len(feed.entries)}")

    if feed.entries:
        print("\nFirst 3 articles:")
        for i, entry in enumerate(feed.entries[:3]):
            print(f"{i+1}. {entry.get('title', 'No title')}")
            print(f"   Published: {entry.get('published', 'No date')}")
            print()

    # Now test with longer timeframe
    print("\n" + "="*80)
    print("Testing article scraping with 720 hours (30 days):")
    articles: List[ScienceDailyArticle] = scraper.get_articles(hours=720)

    print(f"Found {len(articles)} articles")
    print()

    for article in articles:
        print(f"Title: {article.title}")
        print(f"Published: {article.published_at}")
        print(f"Category: {article.category}")
        print(f"URL: {article.url}")
        print(f"Description: {article.description[:100]}...")
        print("-" * 80)
        print()
