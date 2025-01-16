# vector_db/db_manager.py

import os
import pinecone

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "YOUR_PINECONE_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV", "YOUR_ENV")
INDEX_NAME = "veritas-rss"

def init_pinecone():
    # Initialize Pinecone
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(name=INDEX_NAME, dimension=1536)  # dimension depends on embedding model
    return pinecone.Index(INDEX_NAME)

def upsert_articles(index, articles_with_embeddings):
    """
    articles_with_embeddings: list of dicts with:
        {
          "id": str,  # unique ID for the article
          "embedding": List[float],
          "metadata": dict with article metadata
        }
    """
    vectors = []
    for item in articles_with_embeddings:
        vectors.append((
            item["id"],
            item["embedding"],
            item["metadata"]
        ))

    index.upsert(vectors=vectors)