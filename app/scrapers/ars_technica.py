from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel


class ArsTechnicaArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class ArsTechnicaScraper:
    def __init__(self):
        # Ars Technica AI section feed
        self.rss_url = "https://feeds.arstechnica.com/arstechnica/technology-lab"

    def get_articles(self, hours: int = 24) -> List[ArsTechnicaArticle]:
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
                # Filter for AI-related articles
                title = entry.get("title", "").lower()
                description = entry.get("summary", entry.get("description", "")).lower()
                tags = [t.get("term", "").lower() for t in entry.get("tags", [])]

                ai_keywords = ["ai", "artificial intelligence", "machine learning", "deep learning",
                              "neural network", "gpt", "llm", "chatbot", "openai", "anthropic",
                              "google ai", "microsoft ai", "claude", "gemini", "copilot"]

                is_ai_related = any(kw in title or kw in description or kw in " ".join(tags)
                                   for kw in ai_keywords)

                if is_ai_related:
                    articles.append(ArsTechnicaArticle(
                        title=entry.get("title", ""),
                        description=entry.get("summary", entry.get("description", "")),
                        url=entry.get("link", ""),
                        guid=entry.get("id", entry.get("link", "")),
                        published_at=published_time,
                        category=tags[0] if tags else None
                    ))

        return articles


if __name__ == "__main__":
    scraper = ArsTechnicaScraper()
    articles = scraper.get_articles(hours=168)  # Last week
    print(f"Found {len(articles)} AI-related articles from Ars Technica")
    for article in articles[:5]:
        print(f"- {article.title}")
        print(f"  {article.url}")
        print()
