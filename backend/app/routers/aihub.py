from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.ai_insight import AIInsight
from app.models.ai_module import AIModule
from app.models.ai_site_status import AISiteStatus
from app.models.user import User
from app.schemas.ai_insight import AIInsightOut
from app.schemas.ai_module import AIModuleOut
from app.schemas.ai_site_status import AISiteStatusOut

router = APIRouter(prefix="/api/aihub", tags=["aihub"])


@router.get("/overview", response_model=AISiteStatusOut)
def overview(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    row = (
        db.query(AISiteStatus)
        .order_by(desc(AISiteStatus.updated_at), desc(AISiteStatus.id))
        .first()
    )
    if row is None:
        row = AISiteStatus(id=0, monitoring="24/7", zones=0, sensor_health=0)
    return row


@router.get("/modules", response_model=list[AIModuleOut])
def modules(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(AIModule).order_by(AIModule.sort_order.asc(), AIModule.id.asc()).all()


@router.get("/insights", response_model=list[AIInsightOut])
def insights(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(AIInsight).order_by(AIInsight.sort_order.asc(), AIInsight.id.asc()).all()
