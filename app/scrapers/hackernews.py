from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel


class HackerNewsArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class HackerNewsScraper:
    def __init__(self):
        # Hacker News front page RSS (via hnrss.org)
        self.rss_url = "https://hnrss.org/frontpage"

    def get_articles(self, hours: int = 24) -> List[HackerNewsArticle]:
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

                ai_keywords = ["ai", "artificial intelligence", "machine learning", "deep learning",
                              "neural network", "gpt", "llm", "chatbot", "openai", "anthropic",
                              "claude", "gemini", "llama", "mistral", "transformer", "diffusion",
                              "stable diffusion", "midjourney", "dall-e", "copilot", "ml model"]

                is_ai_related = any(kw in title or kw in description for kw in ai_keywords)

                if is_ai_related:
                    # Get the actual article URL (not the HN comments link)
                    url = entry.get("link", "")
                    # hnrss includes the original URL in the comments field
                    if hasattr(entry, "comments"):
                        # The link field has the article, comments has HN discussion
                        pass  # Keep entry.link as is

                    articles.append(HackerNewsArticle(
                        title=entry.get("title", ""),
                        description=entry.get("summary", entry.get("description", "")),
                        url=url,
                        guid=entry.get("id", url),
                        published_at=published_time,
                        category="Hacker News"
                    ))

        return articles


if __name__ == "__main__":
    scraper = HackerNewsScraper()
    articles = scraper.get_articles(hours=168)  # Last week
    print(f"Found {len(articles)} AI-related articles from Hacker News")
    for article in articles[:5]:
        print(f"- {article.title}")
        print(f"  {article.url}")
        print()
