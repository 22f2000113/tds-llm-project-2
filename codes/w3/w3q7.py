from fastapi import HTTPException
from models import SimilarityRequest,SimilarityResponse
from llm_api import get_embedding
import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def get_similarity(request: SimilarityRequest):
    try:
        # Compute embeddings for all documents
        words = request.docs
        words.insert(0, request.query)
        result = get_embedding(words)
        print(result)
        # Compute cosine similarity between query and each document
        similarities = [cosine_similarity(result['data'][0]['embedding'], doc_emb['embedding']) for doc_emb in
                        result['data'][1:]]

        # Get indices of top 3 most similar documents
        top_indices = np.argsort(similarities)[-3:][::-1]

        # Retrieve top 3 matching documents
        top_matches = [request.docs[i] for i in top_indices]
        print("matches ", top_matches)
        return {"matches": top_matches}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
