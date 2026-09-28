from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.kpi import KPI
from app.models.risk_summary import RiskSummary
from app.models.user import User
from app.schemas.kpi import KPIOut
from app.schemas.risk_summary import RiskSummaryOut

router = APIRouter(prefix="/api/risks", tags=["risks"])


@router.get("/kpis", response_model=KPIOut)
def get_risk_kpis(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    kpi = (
        db.query(KPI)
        .order_by(desc(KPI.updated_at), desc(KPI.id))
        .first()
    )
    if kpi is None:
        kpi = KPI(
            id=0,
            overall_risk_score=0,
            risk_label="Unknown",
            safety_compliance=0,
            active_hazards=0,
            live_alerts=0,
        )
    return kpi


@router.get("/summary", response_model=list[RiskSummaryOut])
def get_risk_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(RiskSummary).order_by(RiskSummary.sort_order.asc(), RiskSummary.id.asc()).all()
