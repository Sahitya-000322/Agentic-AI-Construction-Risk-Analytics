from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utc_now


class AIModule(Base):
    __tablename__ = "ai_modules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    metric_label: Mapped[str] = mapped_column(String(50), nullable=False)
    metric_value: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="Active", nullable=False)
    icon_key: Mapped[str] = mapped_column(String(50), default="robot", nullable=False)
    color: Mapped[str] = mapped_column(String(20), default="#2563EB", nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
