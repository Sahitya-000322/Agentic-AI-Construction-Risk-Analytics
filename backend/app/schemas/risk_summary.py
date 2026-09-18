from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RiskSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    count: int
    severity: str
    sort_order: int
    created_at: datetime
