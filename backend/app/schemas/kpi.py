from datetime import datetime

from pydantic import BaseModel, ConfigDict


class KPIOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    overall_risk_score: int
    risk_label: str
    safety_compliance: int
    active_hazards: int
    live_alerts: int
    updated_at: datetime
