from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.performance_metric import PerformanceMetric
from app.models.report import Report
from app.models.user import User
from app.schemas.performance_metric import PerformanceMetricOut
from app.schemas.report import ReportInsightOut, ReportOut, ReportSummaryOut


router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("", response_model=list[ReportOut])
def list_reports(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Report).order_by(Report.sort_order.asc(), Report.id.asc()).all()


@router.get("/summary", response_model=ReportSummaryOut)
def get_summary(_: User = Depends(get_current_user)):
    return ReportSummaryOut(
        total_reports=24,
        safety_score=96,
        risk_events=14,
        ai_insights=38,
    )


@router.get("/performance", response_model=list[PerformanceMetricOut])
def get_performance(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(PerformanceMetric).order_by(PerformanceMetric.sort_order.asc()).all()


@router.get("/insight", response_model=ReportInsightOut)
def get_insight(_: User = Depends(get_current_user)):
    return ReportInsightOut(
        text=(
            "Overall project performance remains stable. "
            "Safety compliance is above target, while schedule health requires "
            "additional monitoring due to increasing structural activity risks."
        ),
        ai_confidence=94,
    )
