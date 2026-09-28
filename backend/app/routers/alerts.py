from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.alert import Alert
from app.models.user import User
from app.schemas.alert import AlertOut

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Alert).order_by(Alert.sort_order.asc(), Alert.id.asc()).all()


@router.get("/notifications", response_model=list[AlertOut])
def list_notifications(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = (
        db.query(Alert)
        .filter(Alert.status == "active")
        .order_by(Alert.sort_order.asc(), Alert.id.asc())
        .limit(3)
        .all()
    )
    return rows
