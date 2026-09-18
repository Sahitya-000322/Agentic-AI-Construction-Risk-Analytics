from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utc_now


class RiskTrend(Base):
    __tablename__ = "risk_trends"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    day: Mapped[str] = mapped_column(String(20), nullable=False)
    value: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
