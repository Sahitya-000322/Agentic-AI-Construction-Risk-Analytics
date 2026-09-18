from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AIInsightOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    color: str
    sort_order: int
    created_at: datetime
