from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HazardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    location: str | None = None
    time_ago: str | None = None
    severity: str
    status: str
    icon_key: str
    sort_order: int
    created_at: datetime
