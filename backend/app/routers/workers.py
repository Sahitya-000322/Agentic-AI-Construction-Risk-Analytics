from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.worker import Worker


router = APIRouter(
    prefix="/api/workers",
    tags=["workers"]
)


class WorkerCreate(BaseModel):
    employee_code: str
    full_name: str
    department: str | None = None


class WorkerOut(BaseModel):
    id: int
    employee_code: str
    full_name: str
    department: str | None
    active: bool

    model_config = {
        "from_attributes": True
    }


@router.post(
    "",
    response_model=WorkerOut
)
def create_worker(
    payload: WorkerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    existing = (
        db.query(Worker)
        .filter(
            Worker.employee_code == payload.employee_code
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Employee code already exists"
        )

    worker = Worker(
        employee_code=payload.employee_code,
        full_name=payload.full_name,
        department=payload.department,
        active=True,
    )

    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker


@router.get(
    "",
    response_model=list[WorkerOut]
)
def list_workers(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):

    return (
        db.query(Worker)
        .order_by(Worker.id.asc())
        .all()
    )