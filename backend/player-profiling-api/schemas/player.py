from typing import Dict

from pydantic import BaseModel, Field


class PlayerStats(BaseModel):
    points: float = Field(..., description="Average points per game")
    assists: float = Field(..., description="Average assists per game")
    rebounds: float = Field(..., description="Average rebounds per game")


class Player(BaseModel):
    player_id: str
    season: int
    stats: PlayerStats


class PlayerProfile(BaseModel):
    player: Dict
    features: Dict
    embedding: Dict
    cluster: Dict
    similarity: Dict
