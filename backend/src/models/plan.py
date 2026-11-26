from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Plan(Base):
    __tablename__ = "plans"

    plan_id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.trip_id")
    )

    status: Mapped[str] = mapped_column(String(50))

    total_estimated_cost: Mapped[Decimal] = mapped_column(
        Numeric(12, 2)
    )

    generation_reason: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    activated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    # Relationships
    trip: Mapped["Trip"] = relationship(back_populates="plans")

    plan_items: Mapped[list["PlanItem"]] = relationship(
        back_populates="plan"
    )

    replanning_requests: Mapped[list["ReplanningRequest"]] = relationship(
        back_populates="current_plan",
        foreign_keys="ReplanningRequest.current_plan_id"
    )

    resulting_replanning_requests: Mapped[list["ReplanningRequest"]] = relationship(
        back_populates="resulting_plan",
        foreign_keys="ReplanningRequest.resulting_plan_id"
    )

    feedback: Mapped[list["Feedback"]] = relationship(
        back_populates="plan"
    )