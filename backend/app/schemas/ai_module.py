from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AIModuleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    metric_label: str
    metric_value: str
    status: str
    icon_key: str
    color: str
    sort_order: int
    created_at: datetime
