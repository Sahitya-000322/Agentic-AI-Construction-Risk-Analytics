from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.ai_site_status import AISiteStatus
from app.models.incident import Incident
from app.models.kpi import KPI
from app.models.milestone import Milestone
from app.models.risk_summary import RiskSummary
from app.models.risk_trend import RiskTrend
from app.models.user import User
from app.schemas.ai_site_status import AISiteStatusOut
from app.schemas.dashboard import (
    ProjectProgressItem,
    ProjectProgressOut,
    RiskDistributionItem,
    RiskDistributionOut,
    RiskGaugeOut,
)
from app.schemas.incident import IncidentOut
from app.schemas.kpi import KPIOut
from app.schemas.risk_summary import RiskSummaryOut
from app.schemas.risk_trend import RiskTrendOut, RiskTrendPoint


router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def _risk_level(value: int) -> str:
    if value < 40:
        return "Low Risk"
    if value < 70:
        return "Medium Risk"
    return "High Risk"


@router.get("/kpis", response_model=KPIOut)
def get_kpis(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    kpi = db.query(KPI).order_by(desc(KPI.id)).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="No KPI data available")
    return kpi


@router.get("/project-progress", response_model=ProjectProgressOut)
def get_project_progress(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(Milestone).order_by(Milestone.sort_order.asc(), Milestone.id.asc()).all()
    if not rows:
        raise HTTPException(status_code=404, detail="No milestone data available")
    phases = [ProjectProgressItem(phase=m.name, value=m.progress) for m in rows]
    return ProjectProgressOut(phases=phases)


@router.get("/risk-gauge", response_model=RiskGaugeOut)
def get_risk_gauge(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    kpi = db.query(KPI).order_by(desc(KPI.id)).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="No KPI data available")
    return RiskGaugeOut(value=kpi.overall_risk_score, level=_risk_level(kpi.overall_risk_score))


@router.get("/risk-trend", response_model=RiskTrendOut)
def get_risk_trend(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    rows = (
        db.query(RiskTrend)
        .order_by(RiskTrend.sort_order.asc(), RiskTrend.id.asc())
        .limit(days)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No risk trend data available")
    data = [RiskTrendPoint(day=r.day, value=r.value) for r in rows]
    current = data[-1].value
    previous = data[-2].value if len(data) >= 2 else current
    return RiskTrendOut(current=current, previous=previous, change=current - previous, data=data)


@router.get("/risk-summary", response_model=list[RiskSummaryOut])
def get_risk_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(RiskSummary).order_by(RiskSummary.sort_order.asc(), RiskSummary.id.asc()).all()
    if not rows:
        raise HTTPException(status_code=404, detail="No risk summary data available")
    return rows


@router.get("/incidents", response_model=list[IncidentOut])
def get_incidents(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(Incident).order_by(Incident.sort_order.asc(), Incident.id.asc()).all()
    if not rows:
        raise HTTPException(status_code=404, detail="No incident data available")
    return rows


@router.get("/ai-site-status", response_model=AISiteStatusOut)
def get_ai_site_status(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    row = db.query(AISiteStatus).order_by(desc(AISiteStatus.id)).first()
    if not row:
        raise HTTPException(status_code=404, detail="No AI site status available")
    return row


@router.get("/risk-distribution", response_model=RiskDistributionOut)
def get_risk_distribution(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(RiskSummary).order_by(RiskSummary.sort_order.asc()).all()
    total = sum(r.count for r in rows) or 1
    dist = [
        RiskDistributionItem(
            label=r.label,
            count=r.count,
            percent=int((r.count / total) * 100),
        )
        for r in rows
    ]
    return RiskDistributionOut(distribution=dist)
