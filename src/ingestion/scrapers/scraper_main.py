from .site_scraper_config import RSS_CONFIGS
from .rss_scraper import fetch_rss_feed
from ..utils.logger import AppLogger

logger = AppLogger(__name__)

def run_all_scrapers():
    all_articles = []

    for rss_config in RSS_CONFIGS:
        logger.info(f"Scraping {rss_config['name']}")
        site_articles = fetch_rss_feed(rss_config['url'])
        logger.info(f"Found {len(site_articles)} articles from {rss_config['name']}")
        
        # TODO: store site_articles in MinIO, DB, or local files
        # For example:
        # store_in_minio(rss_config["name"], site_articles)
        # update_metadata_db(site_articles)

        all_articles.extend(site_articles)

    logger.info(f"Total articles from all sites: {len(all_articles)}")

if __name__ == "__main__":
    run_all_scrapers()