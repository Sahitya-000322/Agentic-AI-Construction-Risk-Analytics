from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.user import utc_now


class Attendance(Base):
    __tablename__ = "attendance"

    __table_args__ = (
        UniqueConstraint(
            "worker_id",
            "attendance_date",
            name="uq_worker_attendance_date",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id"),
        nullable=False,
        index=True
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )

    check_in: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )

    helmet: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    vest: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    gloves: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    boots: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )

    ppe_status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False
    )

    risk: Mapped[str] = mapped_column(
        String(20),
        default="Unknown",
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="present",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False
    )