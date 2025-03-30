from pydantic import BaseModel
from typing import List

class SimilarityRequest(BaseModel):
    docs: List[str]  # Array of document contents
    query: str  # Query string

class SimilarityResponse(BaseModel):
    matches: List[str]