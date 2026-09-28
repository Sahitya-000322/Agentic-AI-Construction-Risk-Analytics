from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.attendance import Attendance
from app.models.user import User


router = APIRouter(
    prefix="/api/attendance",
    tags=["attendance"]
)


@router.get("/today")
def today_attendance(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    today = date.today()

    rows = (
        db.query(Attendance)
        .filter(
            Attendance.attendance_date == today
        )
        .order_by(
            Attendance.check_in.asc()
        )
        .all()
    )

    return rows