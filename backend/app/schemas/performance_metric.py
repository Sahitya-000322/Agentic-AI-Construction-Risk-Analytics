from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PerformanceMetricOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
    value: str
    target: str
    color: str
    sort_order: int
    created_at: datetime
