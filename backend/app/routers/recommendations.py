from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.recommendation import Recommendation
from app.models.user import User
from app.schemas.recommendation import RecommendationOut

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("", response_model=list[RecommendationOut])
def list_recommendations(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Recommendation).order_by(Recommendation.sort_order.asc(), Recommendation.id.asc()).all()
