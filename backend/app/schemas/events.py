from pydantic import BaseModel
from typing import List

class TacticalEvent(BaseModel):
    event_id: str
    timestamp: float
    event_type: str  # e.g., "pass", "shot", "interception"
    description: str # e.g., "Pass completed from Player 10 to Player 9"
    involved_entity_ids: List[int]
