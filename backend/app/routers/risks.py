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
    kpi = db.query(KPI).order_by(desc(KPI.id)).first()
    if not kpi:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No KPI data available")
    return kpi


@router.get("/summary", response_model=list[RiskSummaryOut])
def get_risk_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(RiskSummary).order_by(RiskSummary.sort_order.asc()).all()
