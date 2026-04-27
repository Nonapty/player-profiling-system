from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None


class FeatureVector(BaseModel):
    player_id: str
    vector: List[float]


class Embedding(BaseModel):
    player_id: str
    embedding: List[float]


class ClusterResult(BaseModel):
    player_id: str
    cluster_id: int


class SimilarityResult(BaseModel):
    player_id: str
    similar_players: List[str]


class TrendResult(BaseModel):
    player_id: str
    values: List[float]


class ExplanationResult(BaseModel):
    player_id: str
    explanation: str


class ComparisonResult(BaseModel):
    player1: str
    player2: str
    diff: Dict[str, float]
