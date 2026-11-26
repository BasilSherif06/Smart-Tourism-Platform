from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class LockedBooking(Base):
    __tablename__ = "locked_bookings"

    locked_booking_id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.trip_id")
    )

    place_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("places.place_id")
    )

    title: Mapped[str] = mapped_column(String(255))

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )

    end_datetime: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )

    booking_reference: Mapped[Optional[str]] = mapped_column(String(255))

    status: Mapped[str] = mapped_column(String(50))

    notes: Mapped[Optional[str]] = mapped_column(Text)

    # Relationships
    trip: Mapped["Trip"] = relationship(back_populates="locked_bookings")

    place: Mapped[Optional["Place"]] = relationship(
        back_populates="locked_bookings"
    )