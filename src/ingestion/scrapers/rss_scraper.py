import feedparser
from typing import List, Dict


def fetch_rss_feed(feed_url: str) -> List[Dict]:
    """
    Fetches articles from an RSS feed URL in the provided format.
    Returns a list of dictionaries containing article information.
    """
    articles = []

    try:
        # Parse the RSS feed
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            raise Exception(f"Error parsing RSS feed: {feed.bozo_exception}")

        # Extract relevant data from each entry
        for entry in feed.entries:
            title = entry.title.strip()
            link = entry.link.strip()
            published = entry.get("published", "No date provided")
            summary = entry.summary.strip()
    
            articles.append({
                "title": title,
                "url": link,
                "published_date": published,
                "summary": summary,
            })

    except Exception as e:
        raise Exception(f"Failed to fetch RSS feed: {e}")

    return articles

