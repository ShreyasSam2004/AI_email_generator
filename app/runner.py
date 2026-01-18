from typing import List
from app.config import YOUTUBE_CHANNELS
from app.scrapers.youtube import YouTubeScraper, ChannelVideo
from app.scrapers.openai import OpenAIScraper, OpenAIArticle
from app.scrapers.anthropic import AnthropicScraper, AnthropicArticle
from app.scrapers.venturebeat import VentureBeatScraper, VentureBeatArticle
from app.scrapers.techcrunch import TechCrunchScraper, TechCrunchArticle
from app.scrapers.sciencedaily import ScienceDailyScraper, ScienceDailyArticle
from app.scrapers.mit_tech_review import MITTechReviewScraper, MITTechReviewArticle
from app.scrapers.wired import WiredScraper, WiredArticle
from app.scrapers.ars_technica import ArsTechnicaScraper, ArsTechnicaArticle
from app.scrapers.theverge import TheVergeScraper, TheVergeArticle
from app.scrapers.hackernews import HackerNewsScraper, HackerNewsArticle
from app.database.repository import Repository


def run_scrapers(hours: int = 24) -> dict:
    youtube_scraper = YouTubeScraper()
    openai_scraper = OpenAIScraper()
    anthropic_scraper = AnthropicScraper()
    venturebeat_scraper = VentureBeatScraper()
    techcrunch_scraper = TechCrunchScraper()
    sciencedaily_scraper = ScienceDailyScraper()
    mit_scraper = MITTechReviewScraper()
    wired_scraper = WiredScraper()
    ars_scraper = ArsTechnicaScraper()
    theverge_scraper = TheVergeScraper()
    hackernews_scraper = HackerNewsScraper()
    repo = Repository()

    youtube_videos = []
    video_dicts = []
    for channel_id in YOUTUBE_CHANNELS:
        videos = youtube_scraper.get_latest_videos(channel_id, hours=hours)
        youtube_videos.extend(videos)
        video_dicts.extend([
            {
                "video_id": v.video_id,
                "title": v.title,
                "url": v.url,
                "channel_id": channel_id,
                "published_at": v.published_at,
                "description": v.description,
                "transcript": v.transcript
            }
            for v in videos
        ])

    openai_articles = openai_scraper.get_articles(hours=hours)
    anthropic_articles = anthropic_scraper.get_articles(hours=hours)
    venturebeat_articles = venturebeat_scraper.get_articles(hours=hours)
    techcrunch_articles = techcrunch_scraper.get_articles(hours=hours)
    sciencedaily_articles = sciencedaily_scraper.get_articles(hours=hours)
    mit_articles = mit_scraper.get_articles(hours=hours)
    wired_articles = wired_scraper.get_articles(hours=hours)
    ars_articles = ars_scraper.get_articles(hours=hours)
    theverge_articles = theverge_scraper.get_articles(hours=hours)
    hackernews_articles = hackernews_scraper.get_articles(hours=hours)
    
    if video_dicts:
        repo.bulk_create_youtube_videos(video_dicts)
    
    if openai_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in openai_articles
        ]
        repo.bulk_create_openai_articles(article_dicts)
    
    if anthropic_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in anthropic_articles
        ]
        repo.bulk_create_anthropic_articles(article_dicts)

    if venturebeat_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in venturebeat_articles
        ]
        repo.bulk_create_venturebeat_articles(article_dicts)

    if techcrunch_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in techcrunch_articles
        ]
        repo.bulk_create_techcrunch_articles(article_dicts)

    if sciencedaily_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in sciencedaily_articles
        ]
        repo.bulk_create_sciencedaily_articles(article_dicts)

    if mit_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in mit_articles
        ]
        repo.bulk_create_mit_tech_review_articles(article_dicts)

    if wired_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in wired_articles
        ]
        repo.bulk_create_wired_articles(article_dicts)

    if ars_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in ars_articles
        ]
        repo.bulk_create_ars_technica_articles(article_dicts)

    if theverge_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in theverge_articles
        ]
        repo.bulk_create_theverge_articles(article_dicts)

    if hackernews_articles:
        article_dicts = [
            {
                "guid": a.guid,
                "title": a.title,
                "url": a.url,
                "published_at": a.published_at,
                "description": a.description,
                "category": a.category
            }
            for a in hackernews_articles
        ]
        repo.bulk_create_hackernews_articles(article_dicts)

    return {
        "youtube": youtube_videos,
        "openai": openai_articles,
        "anthropic": anthropic_articles,
        "venturebeat": venturebeat_articles,
        "techcrunch": techcrunch_articles,
        "sciencedaily": sciencedaily_articles,
        "mit_tech_review": mit_articles,
        "wired": wired_articles,
        "ars_technica": ars_articles,
        "theverge": theverge_articles,
        "hackernews": hackernews_articles,
    }


if __name__ == "__main__":
    results = run_scrapers(hours=24)
    print(f"YouTube videos: {len(results['youtube'])}")
    print(f"OpenAI articles: {len(results['openai'])}")
    print(f"Anthropic articles: {len(results['anthropic'])}")
    print(f"VentureBeat articles: {len(results['venturebeat'])}")
    print(f"TechCrunch articles: {len(results['techcrunch'])}")
    print(f"ScienceDaily articles: {len(results['sciencedaily'])}")
    print(f"MIT Tech Review articles: {len(results['mit_tech_review'])}")
    print(f"Wired articles: {len(results['wired'])}")
    print(f"Ars Technica articles: {len(results['ars_technica'])}")
    print(f"The Verge articles: {len(results['theverge'])}")
    print(f"Hacker News articles: {len(results['hackernews'])}")
