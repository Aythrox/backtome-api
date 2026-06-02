from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Sighting(BaseModel):
    sighting_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Primary Key")
    alert_id: str = Field(..., description="GSI1 Partition Key")
    spotter_id: str
    latitude: float
    longitude: float
    photo_url: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="GSI1 Sort Key")
