from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from docling.document_converter import DocumentConverter
from pydantic import BaseModel


class AnthropicArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class AnthropicScraper:
    def __init__(self):
        self.rss_urls = [
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        ]
        self.converter = DocumentConverter()

    def get_articles(self, hours: int = 24) -> List[AnthropicArticle]:
        now = datetime.now(timezone.utc)
        cutoff_time = now - timedelta(hours=hours)
        articles = []
        seen_guids = set()
        
        for rss_url in self.rss_urls:
            feed = feedparser.parse(rss_url)
            if not feed.entries:
                continue
            
            for entry in feed.entries:
                published_parsed = getattr(entry, "published_parsed", None)
                if not published_parsed:
                    continue
                
                published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)
                if published_time >= cutoff_time:
                    guid = entry.get("id", entry.get("link", ""))
                    if guid not in seen_guids:
                        seen_guids.add(guid)
                        articles.append(AnthropicArticle(
                            title=entry.get("title", ""),
                            description=entry.get("description", ""),
                            url=entry.get("link", ""),
                            guid=guid,
                            published_at=published_time,
                            category=entry.get("tags", [{}])[0].get("term") if entry.get("tags") else None
                        ))
        
        return articles

    def url_to_markdown(self, url: str) -> Optional[str]:
        try:
            result = self.converter.convert(url)
            return result.document.export_to_markdown()
        except Exception:
            return None

if __name__ == "__main__":
    scraper = AnthropicScraper()
    
    # Debug: Check what's in the feeds
    print("Debugging RSS feeds:")
    for i, rss_url in enumerate(scraper.rss_urls):
        feed = feedparser.parse(rss_url)
        print(f"\nFeed {i+1}: {rss_url.split('/')[-1]}")
        print(f"Total entries: {len(feed.entries)}")
        if feed.entries:
            print(f"First entry: {feed.entries[0].get('title', 'No title')}")
            print(f"Published: {feed.entries[0].get('published', 'No date')}")
    
    print("\n" + "="*80)
    print("Testing article scraping with 720 hours (30 days):")
    articles: List[AnthropicArticle] = scraper.get_articles(hours=720)
    
    print(f"Found {len(articles)} articles")
    print()
    
    if articles:
        for article in articles:
            print(f"Title: {article.title}")
            print(f"Published: {article.published_at}")
            print(f"URL: {article.url}")
            print(f"Description: {article.description}")  # Add this line
            print("-" * 80)
            print()
        
        # Test markdown conversion on first article
        print("\n" + "="*80)
        print("Testing markdown conversion on first article:")
        print(f"Converting: {articles[0].url}")
        markdown = scraper.url_to_markdown(articles[0].url)
        if markdown:
            print(f"Success! Markdown length: {len(markdown)} characters")
            print("\nFirst 500 characters:")
            print(markdown)
        else:
            print("Failed to convert to markdown")
    else:
        print("No articles found. Try increasing the hours parameter.")