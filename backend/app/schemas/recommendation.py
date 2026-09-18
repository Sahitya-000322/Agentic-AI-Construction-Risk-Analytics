from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecommendationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action: str
    description: str
    priority: str
    category: str | None = None
    icon_key: str
    sort_order: int
    created_at: datetime
