# scrapers/scraper_main.py

from scrapers.site_scraper_config import SITE_CONFIGS
from scrapers.site_scraper import scrape_website
from utils.logger import get_logger

logger = get_logger(__name__)

def run_all_scrapers():
    all_articles = []

    for site_config in SITE_CONFIGS:
        logger.info(f"Scraping {site_config['name']} ...")
        site_articles = scrape_website(site_config)
        logger.info(f"Found {len(site_articles)} articles from {site_config['name']}")
        
        # TODO: store site_articles in MinIO, DB, or local files
        # For example:
        # store_in_minio(site_config["name"], site_articles)
        # update_metadata_db(site_articles)

        all_articles.extend(site_articles)

    logger.info(f"Total articles from all sites: {len(all_articles)}")

if __name__ == "__main__":
    run_all_scrapers()