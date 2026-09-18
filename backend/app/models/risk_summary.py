from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utc_now


class RiskSummary(Base):
    __tablename__ = "risk_summary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
