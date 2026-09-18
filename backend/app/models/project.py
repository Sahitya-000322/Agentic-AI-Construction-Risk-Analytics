from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utc_now


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    color: Mapped[str] = mapped_column(String(20), default="#3B82F6", nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)
    days_left: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    budget: Mapped[str | None] = mapped_column(String(50), nullable=True)
    workers_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    deadline: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
