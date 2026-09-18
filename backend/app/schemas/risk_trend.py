from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RiskTrendPoint(BaseModel):
    day: str
    value: int = Field(..., ge=0, le=100)


class RiskTrendOut(BaseModel):
    current: int
    previous: int
    change: int
    data: list[RiskTrendPoint]
