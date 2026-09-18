from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AISiteStatusOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    monitoring: str
    zones: int
    sensor_health: int
    updated_at: datetime
