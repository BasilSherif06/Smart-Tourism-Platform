from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class DisruptionEvent(Base):
    __tablename__ = "disruption_events"

    disruption_id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.trip_id")
    )

    place_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("places.place_id")
    )

    reported_by_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.user_id")
    )

    disruption_type: Mapped[str] = mapped_column(String(100))

    description: Mapped[str] = mapped_column(Text)

    severity: Mapped[str] = mapped_column(String(50))

    start_datetime: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    end_datetime: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    source_name: Mapped[Optional[str]] = mapped_column(String(150))

    source_reference: Mapped[Optional[str]] = mapped_column(String(255))

    status: Mapped[str] = mapped_column(String(50))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    trip: Mapped["Trip"] = relationship(
        back_populates="disruption_events"
    )

    place: Mapped[Optional["Place"]] = relationship(
        back_populates="disruption_events"
    )

    reported_by: Mapped[Optional["User"]] = relationship(
        back_populates="reported_disruptions"
    )

    replanning_requests: Mapped[list["ReplanningRequest"]] = relationship(
        back_populates="disruption"
    )