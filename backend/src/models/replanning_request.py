from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class ReplanningRequest(Base):
    __tablename__ = "replanning_requests"

    replanning_request_id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.trip_id")
    )

    disruption_id: Mapped[int] = mapped_column(
        ForeignKey("disruption_events.disruption_id")
    )

    current_plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.plan_id")
    )

    resulting_plan_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("plans.plan_id")
    )

    requested_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.user_id")
    )

    reason: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    # Relationships
    trip: Mapped["Trip"] = relationship(
        back_populates="replanning_requests"
    )

    disruption: Mapped["DisruptionEvent"] = relationship(
        back_populates="replanning_requests"
    )

    current_plan: Mapped["Plan"] = relationship(
        back_populates="replanning_requests",
        foreign_keys=[current_plan_id]
    )

    resulting_plan: Mapped[Optional["Plan"]] = relationship(
        back_populates="resulting_replanning_requests",
        foreign_keys=[resulting_plan_id]
    )

    requested_by: Mapped[Optional["User"]] = relationship(
        back_populates="replanning_requests"
    )

    decision_records: Mapped[list["DecisionRecord"]] = relationship(
        back_populates="replanning_request"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="replanning_request"
    )