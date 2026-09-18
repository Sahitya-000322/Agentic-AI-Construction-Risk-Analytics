from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ZoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    area: str | None = None
    risk_level: str
    sort_order: int
    created_at: datetime
