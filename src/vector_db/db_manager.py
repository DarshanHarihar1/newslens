import os
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from utils.load_config import load_config

CONFIG_PATH = "newslens/configs/config_map.YAML"

config = load_config(CONFIG_PATH)  

PINECONE_API_KEY = config["data"].get("PINECONE_API_KEY")
PINECONE_ENV = config["data"].get("PINECONE_ENV", "us-west-1")

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "pcsk_2BFn6U_DaTpsuiJkUfvp9hvAwe7C5ztnb4KS9MRB4zoYTWLdjS4nzrQZkjAEi4TCXaxq5D")
# PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")  # or whichever region you use
INDEX_NAME = "veritas-rss"

class PineconeClient:
    def __init__(self, index_name=INDEX_NAME):
        # Create a Pinecone instance
        # API key is mandatory, region is specified via ServerlessSpec
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        
        # Check if the index exists
        existing_indexes = self.pc.list_indexes().names()
        if index_name not in existing_indexes:
            # Create the index with desired dimension and metric
            self.pc.create_index(
                name=index_name,
                dimension=768,             # depends on your embedding model
                metric='cosine',            # or 'dotproduct', 'euclidean'
                spec=ServerlessSpec(
                    cloud='aws',
                    region=PINECONE_ENV      # e.g. 'us-west-1', 'us-east-1', etc.
                )
            )
        
        # Get a handle to the index
        self.index = self.pc.Index(index_name)

    def upsert_articles(self, articles_with_embeddings: List[Dict[str, Any]]):
        """
        articles_with_embeddings: list of dicts with:
            {
                "id": str,            # unique ID for the article
                "embedding": List[float],
                "metadata": dict      # arbitrary metadata about the article
            }
        """
        vectors = []
        for item in articles_with_embeddings:
            vectors.append((
                item["id"],
                item["embedding"],
                item["metadata"]
            ))
        
        self.index.upsert(vectors=vectors)

    def semantic_search(self, query_embedding: List[float], top_k=5):
        """
        Example method for performing a query with an embedding.
        """
        response = self.index.query(vector=query_embedding, top_k=top_k, includeMetadata=True)
        return response.matches