from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    description: str
    location: str | None = None
    time_ago: str | None = None
    severity: str
    icon_key: str
    sort_order: int
    created_at: datetime
