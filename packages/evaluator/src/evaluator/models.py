from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Track(BaseModel):
    title: str
    artist: str


class PlaylistInput(BaseModel):
    prompt: str
    tracks: List[Track]


class ScoreComponent(BaseModel):
    name: str
    value: float
    max_value: float


class EvaluationResult(BaseModel):
    prompt: str
    overall_score: float
    components: List[ScoreComponent]
    evaluated_tracks: List[Track]
