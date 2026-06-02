from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class Message(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Primary Key")
    alert_id: str = Field(..., description="GSI1 Partition Key")
    sender_id: str
    recipient_id: str
    content: str
    is_read: bool = False
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="GSI1 Sort Key")
