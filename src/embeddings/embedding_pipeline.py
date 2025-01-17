from sentence_transformers import SentenceTransformer
from typing import List

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def generate_embedding(text: str) -> List[float]:
    embedding = model.encode(text)
    return embedding.tolist()  