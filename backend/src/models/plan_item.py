from decimal import Decimal
from typing import Optional
from datetime import time

from sqlalchemy import ForeignKey, Integer, Numeric, String, Text, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class PlanItem(Base):
    __tablename__ = "plan_items"

    plan_item_id: Mapped[int] = mapped_column(primary_key=True)

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.plan_id")
    )

    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.place_id")
    )

    day_number: Mapped[int] = mapped_column(Integer)

    start_time: Mapped[Optional[time]] = mapped_column(Time)

    end_time: Mapped[Optional[time]] = mapped_column(Time)

    estimated_duration_minutes: Mapped[Optional[int]]

    estimated_cost: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(12, 2)
    )

    sequence_number: Mapped[int] = mapped_column(Integer)

    status: Mapped[str] = mapped_column(String(50))

    notes: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    plan: Mapped["Plan"] = relationship(back_populates="plan_items")

    place: Mapped["Place"] = relationship(back_populates="plan_items")