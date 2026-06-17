from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid
import geohash2 as gh

class AlertStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"

class Alert(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Primary Key")
    owner_id: str = Field(..., description="GSI1 Partition Key")
    subject_id: str
    status: AlertStatus = AlertStatus.ACTIVE
    
    # Location
    latitude: float
    longitude: float
    geohash: str = Field(default="", description="LocationIndex Sort Key")
    geohash_prefix: str = Field(default="", description="LocationIndex Partition Key. Prefix of length 5 (~5x5km)")
    
    # Details
    last_seen_date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    bounty_reward_amount: Optional[float] = None
    bounty_reward_currency: Optional[str] = None
    description: str = ""
    
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="GSI1 Sort Key")
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    @model_validator(mode='after')
    def compute_geohash(self) -> 'Alert':
        if self.latitude is not None and self.longitude is not None:
            full_geohash = gh.encode(self.latitude, self.longitude, precision=12)
            self.geohash = full_geohash
            # Use prefix of length 5 for clustering (~5km area)
            self.geohash_prefix = full_geohash[:5]
        return self
