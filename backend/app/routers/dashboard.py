from fastapi import APIRouter, Depends

from sqlalchemy import desc

from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies import get_current_user

from app.models.ai_site_status import AISiteStatus
from app.models.alert import Alert
from app.models.hazard import Hazard
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


router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"]
)


def _risk_level(value: int) -> str:

    if value < 40:
        return "Low Risk"

    if value < 70:
        return "Medium Risk"

    return "High Risk"


# ============================================================
# DASHBOARD KPIs
# ============================================================

@router.get("/kpis", response_model=KPIOut)
def get_kpis(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    # Get latest KPI record
    kpi = (
        db.query(KPI)
        .order_by(
            desc(KPI.updated_at),
            desc(KPI.id)
        )
        .first()
    )

    # --------------------------------------------------------
    # ACTIVE HAZARDS
    # --------------------------------------------------------

    active_hazards = (
        db.query(Hazard)
        .filter(
            Hazard.status == "active"
        )
        .count()
    )

    # --------------------------------------------------------
    # LIVE ALERTS
    # --------------------------------------------------------

    live_alerts = (
        db.query(Alert)
        .filter(
            Alert.status == "active"
        )
        .count()
    )

    # --------------------------------------------------------
    # RETURN KPI DATA
    # --------------------------------------------------------

    if kpi:

        return KPIOut(
            id=kpi.id,
            overall_risk_score=kpi.overall_risk_score,
            risk_label=kpi.risk_label,
            safety_compliance=kpi.safety_compliance,
            active_hazards=active_hazards,
            live_alerts=live_alerts,
            updated_at=kpi.updated_at,
        )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    return KPIOut(
        id=0,
        overall_risk_score=0,
        risk_label="Unknown",
        safety_compliance=0,
        active_hazards=active_hazards,
        live_alerts=live_alerts,
        updated_at=None,
    )


# ============================================================
# PROJECT PROGRESS
# ============================================================

@router.get(
    "/project-progress",
    response_model=ProjectProgressOut
)
def get_project_progress(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    rows = (
        db.query(Milestone)
        .order_by(
            Milestone.sort_order.asc(),
            Milestone.id.asc()
        )
        .all()
    )

    phases = [
        ProjectProgressItem(
            phase=m.name,
            value=m.progress
        )
        for m in rows
    ]

    return ProjectProgressOut(
        phases=phases
    )


# ============================================================
# RISK GAUGE
# ============================================================

@router.get(
    "/risk-gauge",
    response_model=RiskGaugeOut
)
def get_risk_gauge(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    kpi = (
        db.query(KPI)
        .order_by(
            desc(KPI.updated_at),
            desc(KPI.id)
        )
        .first()
    )

    value = (
        kpi.overall_risk_score
        if kpi
        else 0
    )

    return RiskGaugeOut(
        value=value,
        level=(
            _risk_level(value)
            if kpi
            else "Unknown"
        )
    )


# ============================================================
# RISK TREND
# ============================================================

@router.get(
    "/risk-trend",
    response_model=RiskTrendOut
)
def get_risk_trend(
    days: int = 7,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    days = max(
        1,
        min(30, days)
    )

    rows = (
        db.query(RiskTrend)
        .order_by(
            RiskTrend.sort_order.asc(),
            RiskTrend.id.asc()
        )
        .limit(days)
        .all()
    )

    data = [
        RiskTrendPoint(
            day=r.day,
            value=r.value
        )
        for r in rows
    ]

    if not data:

        return RiskTrendOut(
            current=0,
            previous=0,
            change=0,
            data=[]
        )

    current = data[-1].value

    previous = (
        data[-2].value
        if len(data) >= 2
        else current
    )

    return RiskTrendOut(
        current=current,
        previous=previous,
        change=current - previous,
        data=data
    )


# ============================================================
# RISK SUMMARY
# ============================================================

@router.get(
    "/risk-summary",
    response_model=list[RiskSummaryOut]
)
def get_risk_summary(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    return (
        db.query(RiskSummary)
        .order_by(
            RiskSummary.sort_order.asc(),
            RiskSummary.id.asc()
        )
        .all()
    )


# ============================================================
# INCIDENTS
# ============================================================

@router.get(
    "/incidents",
    response_model=list[IncidentOut]
)
def get_incidents(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    return (
        db.query(Incident)
        .order_by(
            Incident.sort_order.asc(),
            Incident.id.asc()
        )
        .all()
    )


# ============================================================
# AI SITE STATUS
# ============================================================

@router.get(
    "/ai-site-status",
    response_model=AISiteStatusOut
)
def get_ai_site_status(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    row = (
        db.query(AISiteStatus)
        .order_by(
            desc(AISiteStatus.updated_at),
            desc(AISiteStatus.id)
        )
        .first()
    )

    if row is None:

        row = AISiteStatus(
            id=0,
            monitoring="24/7",
            zones=0,
            sensor_health=0
        )

    return row


# ============================================================
# RISK DISTRIBUTION
# ============================================================

@router.get(
    "/risk-distribution",
    response_model=RiskDistributionOut
)
def get_risk_distribution(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    rows = (
        db.query(RiskSummary)
        .order_by(
            RiskSummary.sort_order.asc()
        )
        .all()
    )

    if not rows:

        return RiskDistributionOut(
            distribution=[]
        )

    total = (
        sum(r.count for r in rows)
        or 1
    )

    dist = [

        RiskDistributionItem(
            label=r.label,
            count=r.count,
            percent=int(
                (r.count / total) * 100
            ),
        )

        for r in rows

    ]

    return RiskDistributionOut(
        distribution=dist
    )