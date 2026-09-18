from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.milestone import Milestone
from app.models.user import User
from app.schemas.milestone import MilestoneOut


router = APIRouter(prefix="/api/milestones", tags=["milestones"])


@router.get("", response_model=list[MilestoneOut])
def list_milestones(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Milestone).order_by(Milestone.sort_order.asc(), Milestone.id.asc()).all()
