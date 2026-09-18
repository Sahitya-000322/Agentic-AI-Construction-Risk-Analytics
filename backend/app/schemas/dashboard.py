from pydantic import BaseModel, Field


class RiskGaugeOut(BaseModel):
    value: int = Field(..., ge=0, le=100)
    level: str


class RiskDistributionItem(BaseModel):
    label: str
    count: int
    percent: int


class RiskDistributionOut(BaseModel):
    distribution: list[RiskDistributionItem]


class ProjectProgressItem(BaseModel):
    phase: str
    value: int = Field(..., ge=0, le=100)


class ProjectProgressOut(BaseModel):
    phases: list[ProjectProgressItem]
