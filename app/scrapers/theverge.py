from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel


class TheVergeArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class TheVergeScraper:
    def __init__(self):
        # The Verge AI section feed
        self.rss_url = "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"

    def get_articles(self, hours: int = 24) -> List[TheVergeArticle]:
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

            if published_time > now:
                published_time = published_time.replace(year=published_time.year - 1)

            if published_time >= cutoff_time:
                articles.append(TheVergeArticle(
                    title=entry.get("title", ""),
                    description=entry.get("summary", entry.get("description", "")),
                    url=entry.get("link", ""),
                    guid=entry.get("id", entry.get("link", "")),
                    published_at=published_time,
                    category="AI"
                ))

        return articles


if __name__ == "__main__":
    scraper = TheVergeScraper()
    articles = scraper.get_articles(hours=168)  # Last week
    print(f"Found {len(articles)} articles from The Verge AI")
    for article in articles[:5]:
        print(f"- {article.title}")
        print(f"  {article.url}")
        print()
