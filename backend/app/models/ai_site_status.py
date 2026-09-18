from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utc_now


class AISiteStatus(Base):
    __tablename__ = "ai_site_status"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    monitoring: Mapped[str] = mapped_column(default="24/7", nullable=False)
    zones: Mapped[int] = mapped_column(Integer, default=32, nullable=False)
    sensor_health: Mapped[int] = mapped_column(Integer, default=98, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
