from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Trip(Base):
    __tablename__ = "trips"

    trip_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id")
    )

    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.city_id")
    )

    start_date: Mapped[date] = mapped_column(Date)

    end_date: Mapped[date] = mapped_column(Date)

    budget: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    status: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="trips")

    city: Mapped["City"] = relationship(back_populates="trips")

    preferences: Mapped[Optional["TripPreference"]] = relationship(
        back_populates="trip", uselist=False
    )

    plans: Mapped[list["Plan"]] = relationship(back_populates="trip")

    locked_bookings: Mapped[list["LockedBooking"]] = relationship(
        back_populates="trip"
    )

    disruption_events: Mapped[list["DisruptionEvent"]] = relationship(
        back_populates="trip"
    )

    replanning_requests: Mapped[list["ReplanningRequest"]] = relationship(
        back_populates="trip"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="trip"
    )

    feedback: Mapped[list["Feedback"]] = relationship(
        back_populates="trip"
    )

    