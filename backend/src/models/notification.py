from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id")
    )

    trip_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("trips.trip_id")
    )

    replanning_request_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("replanning_requests.replanning_request_id")
    )

    notification_type: Mapped[str] = mapped_column(String(100))

    title: Mapped[str] = mapped_column(String(255))

    message: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    read_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="notifications")

    trip: Mapped[Optional["Trip"]] = relationship(
        back_populates="notifications"
    )

    replanning_request: Mapped[Optional["ReplanningRequest"]] = relationship(
        back_populates="notifications"
    )