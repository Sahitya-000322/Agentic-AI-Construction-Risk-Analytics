from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    code: str
    type: str
    generated_at: str
    status: str
    color: str
    sort_order: int
    created_at: datetime


class ReportSummaryOut(BaseModel):
    total_reports: int
    safety_score: int
    risk_events: int
    ai_insights: int


class ReportInsightOut(BaseModel):
    text: str
    ai_confidence: int
