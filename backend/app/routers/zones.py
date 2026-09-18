from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.zone import Zone
from app.schemas.zone import ZoneOut


router = APIRouter(prefix="/api/zones", tags=["zones"])


@router.get("", response_model=list[ZoneOut])
def list_zones(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Zone).order_by(Zone.sort_order.asc(), Zone.id.asc()).all()
