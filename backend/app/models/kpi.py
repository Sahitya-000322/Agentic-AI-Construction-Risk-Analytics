from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utc_now


class KPI(Base):
    __tablename__ = "kpis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    overall_risk_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    risk_label: Mapped[str] = mapped_column(String(20), default="Medium Risk", nullable=False)
    safety_compliance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active_hazards: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    live_alerts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
