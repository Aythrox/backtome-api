from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class SubjectType(str, Enum):
    PET_DOG = "PET_DOG"
    PET_CAT = "PET_CAT"
    HUMAN = "HUMAN"

class Subject(BaseModel):
    subject_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Primary Key")
    owner_id: str = Field(..., description="GSI Partition Key")
    subject_type: SubjectType
    name: str
    weight_kg: Optional[float] = None
    color: Optional[str] = None
    distinguishing_marks: Optional[str] = None
    photo_urls: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="GSI Sort Key")
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
