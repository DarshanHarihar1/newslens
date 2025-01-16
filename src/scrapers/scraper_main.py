# scrapers/scraper_main.py

from .site_scraper_config import RSS_CONFIGS
from .rss_scraper import fetch_rss_feed

from ..utils.logger import AppLogger
from ..embeddings.embedding_pipeline import generate_embedding
from ..vector_db.db_manager import init_pinecone, upsert_articles

import uuid  # for generating unique IDs

logger = AppLogger(__name__)

def run_all_scrapers():
    # Initialize Pinecone index (or another vector DB)
    index = init_pinecone()

    all_articles = []

    for rss_config in RSS_CONFIGS:
        logger.info(f"Fetching RSS feed: {rss_config['name']}")
        site_articles = fetch_rss_feed(rss_config['url'])
        logger.info(f"Found {len(site_articles)} articles from {rss_config['name']}")
        
        # Generate embeddings and prepare for upsert
        articles_with_embeddings = []
        for article in site_articles:
            # Combine title + summary for embedding text
            text_for_embedding = article["title"] + " " + article.get("summary", "")
            embedding = generate_embedding(text_for_embedding)

            # Create a unique ID for each article
            article_id = str(uuid.uuid4())

            # Prepare metadata
            metadata = {
                "title": article["title"],
                "url": article["url"],
                "published_date": article["published_date"],
                "summary": article["summary"],
                "source_name": rss_config["name"]
            }

            articles_with_embeddings.append({
                "id": article_id,
                "embedding": embedding,
                "metadata": metadata
            })

        # Upsert into vector DB
        upsert_articles(index, articles_with_embeddings)
        all_articles.extend(site_articles)

    logger.info(f"Total articles processed: {len(all_articles)}")


if __name__ == "__main__":
    run_all_scrapers()