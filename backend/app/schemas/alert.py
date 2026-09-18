from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    level: str
    time_ago: str | None = None
    status: str
    icon_key: str
    sort_order: int
    created_at: datetime
