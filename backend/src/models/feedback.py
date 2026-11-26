from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Feedback(Base):
    __tablename__ = "feedback"

    feedback_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id")
    )

    trip_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("trips.trip_id")
    )

    plan_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("plans.plan_id")
    )

    rating: Mapped[int] = mapped_column(Integer)

    comments: Mapped[Optional[str]] = mapped_column(Text)

    feedback_type: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="feedback")

    trip: Mapped[Optional["Trip"]] = relationship(
        back_populates="feedback"
    )

    plan: Mapped[Optional["Plan"]] = relationship(
        back_populates="feedback"
    )