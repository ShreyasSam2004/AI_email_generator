import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from app.runner import run_scrapers
from app.services.process_anthropic import process_anthropic_markdown
from app.services.process_youtube import process_youtube_transcripts
from app.services.process_digest import process_digests
from app.services.process_email import send_digest_email

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict:
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("Starting Daily AI News Aggregator Pipeline")
    logger.info("=" * 60)
    
    results = {
        "start_time": start_time.isoformat(),
        "scraping": {},
        "processing": {},
        "digests": {},
        "email": {},
        "success": False
    }
    
    try:
        logger.info("\n[1/5] Scraping articles from sources...")
        scraping_results = run_scrapers(hours=hours)
        results["scraping"] = {
            "youtube": len(scraping_results.get("youtube", [])),
            "openai": len(scraping_results.get("openai", [])),
            "anthropic": len(scraping_results.get("anthropic", [])),
            "venturebeat": len(scraping_results.get("venturebeat", [])),
            "techcrunch": len(scraping_results.get("techcrunch", [])),
            "sciencedaily": len(scraping_results.get("sciencedaily", [])),
            "mit_tech_review": len(scraping_results.get("mit_tech_review", [])),
            "wired": len(scraping_results.get("wired", [])),
            "ars_technica": len(scraping_results.get("ars_technica", [])),
            "theverge": len(scraping_results.get("theverge", [])),
            "hackernews": len(scraping_results.get("hackernews", []))
        }
        total_articles = sum(results["scraping"].values())
        logger.info(f"✓ Scraped {total_articles} total articles:")
        logger.info(f"  - YouTube: {results['scraping']['youtube']}")
        logger.info(f"  - OpenAI: {results['scraping']['openai']}")
        logger.info(f"  - Anthropic: {results['scraping']['anthropic']}")
        logger.info(f"  - VentureBeat: {results['scraping']['venturebeat']}")
        logger.info(f"  - TechCrunch: {results['scraping']['techcrunch']}")
        logger.info(f"  - ScienceDaily: {results['scraping']['sciencedaily']}")
        logger.info(f"  - MIT Tech Review: {results['scraping']['mit_tech_review']}")
        logger.info(f"  - Wired: {results['scraping']['wired']}")
        logger.info(f"  - Ars Technica: {results['scraping']['ars_technica']}")
        logger.info(f"  - The Verge: {results['scraping']['theverge']}")
        logger.info(f"  - Hacker News: {results['scraping']['hackernews']}")
        
        logger.info("\n[2/5] Processing Anthropic markdown...")
        anthropic_result = process_anthropic_markdown()
        results["processing"]["anthropic"] = anthropic_result
        logger.info(f"✓ Processed {anthropic_result['processed']} Anthropic articles "
                    f"({anthropic_result['failed']} failed)")
        
        logger.info("\n[3/5] Processing YouTube transcripts...")
        youtube_result = process_youtube_transcripts()
        results["processing"]["youtube"] = youtube_result
        logger.info(f"✓ Processed {youtube_result['processed']} transcripts "
                    f"({youtube_result['unavailable']} unavailable)")
        
        logger.info("\n[4/5] Creating digests for articles...")
        digest_result = process_digests()
        results["digests"] = digest_result
        logger.info(f"✓ Created {digest_result['processed']} digests "
                    f"({digest_result['failed']} failed out of {digest_result['total']} total)")
        
        logger.info("\n[5/5] Generating and sending email digest...")
        email_result = send_digest_email(hours=hours, top_n=top_n)
        results["email"] = email_result

        if email_result["success"]:
            logger.info(f"✓ Email sent successfully with {email_result['articles_count']} articles")
            results["success"] = True
        elif email_result.get("error") == "No digests available":
            # No news today is not a failure - just nothing to report
            logger.info("ℹ No new content to send today - skipping email")
            results["success"] = True  # Pipeline succeeded, just no content
            results["no_content"] = True
        else:
            logger.error(f"✗ Failed to send email: {email_result.get('error', 'Unknown error')}")
        
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        results["error"] = str(e)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    results["end_time"] = end_time.isoformat()
    results["duration_seconds"] = duration
    
    logger.info("\n" + "=" * 60)
    logger.info("Pipeline Summary")
    logger.info("=" * 60)
    logger.info(f"Duration: {duration:.1f} seconds")
    logger.info(f"Scraped: {results['scraping']}")
    logger.info(f"Processed: {results['processing']}")
    logger.info(f"Digests: {results['digests']}")
    if results.get("no_content"):
        logger.info("Email: Skipped (no new content)")
    else:
        logger.info(f"Email: {'Sent' if results['success'] else 'Failed'}")
    logger.info("=" * 60)
    
    return results


if __name__ == "__main__":
    result = run_daily_pipeline(hours=24, top_n=10)
    exit(0 if result["success"] else 1)
