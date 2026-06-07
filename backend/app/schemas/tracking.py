from pydantic import BaseModel
from typing import List, Optional, Tuple

class Entity(BaseModel):
    id: int
    label: str  # "player", "referee", "ball"
    team: Optional[str] = None  # "team_a", "team_b", or None
    position: Tuple[float, float]  # (x, y) coordinates mapped to the 2D pitch
    speed: Optional[float] = 0.0

class FrameData(BaseModel):
    frame_id: int
    timestamp: float
    entities: List[Entity]
