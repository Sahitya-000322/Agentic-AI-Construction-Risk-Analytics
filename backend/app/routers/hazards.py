from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.hazard import Hazard
from app.models.user import User
from app.schemas.hazard import HazardOut

router = APIRouter(prefix="/api/hazards", tags=["hazards"])


@router.get("", response_model=list[HazardOut])
def list_hazards(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Hazard).order_by(Hazard.sort_order.asc(), Hazard.id.asc()).all()
