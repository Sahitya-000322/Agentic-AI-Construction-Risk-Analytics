from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MilestoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    status: str
    progress: int = Field(..., ge=0, le=100)
    description: str | None = None
    sort_order: int
    created_at: datetime
