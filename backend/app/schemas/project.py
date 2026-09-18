from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectBase(BaseModel):
    name: str
    code: str
    progress: int = Field(..., ge=0, le=100)
    color: str = "#3B82F6"
    risk_level: str = "medium"
    status: str = "active"
    days_left: int = 0
    location: str | None = None
    budget: str | None = None
    workers_count: int = 0
    deadline: str | None = None


class ProjectOut(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class ProjectSummaryOut(BaseModel):
    total_projects: int
    on_schedule: int
    at_risk: int
    completed: int


class ProjectPerformanceOut(BaseModel):
    average_progress: int
    budget_utilization: int
    safety_compliance: int
    schedule_health: int
