from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.project import Project
from app.models.user import User
from app.schemas.project import (
    ProjectOut,
    ProjectPerformanceOut,
    ProjectSummaryOut,
)

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Project).order_by(Project.id.asc()).all()


@router.get("/summary", response_model=ProjectSummaryOut)
def get_summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(Project).all()
    if not rows:
        return ProjectSummaryOut(total_projects=0, on_schedule=0, at_risk=0, completed=0)
    return ProjectSummaryOut(
        total_projects=len(rows),
        on_schedule=sum(
            1 for p in rows
            if p.status.lower() in ("on track", "active") and p.risk_level.lower() != "high"
        ),
        at_risk=sum(
            1 for p in rows
            if p.risk_level.lower() in ("high", "medium") and p.status.lower() == "delayed"
        ),
        completed=sum(1 for p in rows if p.progress >= 100 or p.status.lower() == "completed"),
    )


@router.get("/performance", response_model=ProjectPerformanceOut)
def get_performance(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    rows = db.query(Project).all()
    if not rows:
        return ProjectPerformanceOut(
            average_progress=0, budget_utilization=0, safety_compliance=0, schedule_health=0
        )
    avg_progress = int(sum(p.progress for p in rows) / len(rows))
    return ProjectPerformanceOut(
        average_progress=avg_progress,
        budget_utilization=68,
        safety_compliance=96,
        schedule_health=78,
    )


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    return project
