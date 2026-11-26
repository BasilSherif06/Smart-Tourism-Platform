from datetime import time

from sqlalchemy import ForeignKey, String, Time, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class TripPreference(Base):
    __tablename__ = "trip_preferences"

    __table_args__ = (
        UniqueConstraint("trip_id"),
    )

    trip_preference_id: Mapped[int] = mapped_column(primary_key=True)

    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.trip_id")
    )

    travel_group: Mapped[str] = mapped_column(String(100))

    interests: Mapped[list] = mapped_column(JSON)

    daily_intensity: Mapped[str] = mapped_column(String(50))

    transport_preference: Mapped[str] = mapped_column(String(100))

    accommodation_preference: Mapped[str] = mapped_column(String(100))

    midday_break_preference: Mapped[str] = mapped_column(String(100))

    meal_planning_preference: Mapped[str] = mapped_column(String(100))

    activities_start_time: Mapped[time] = mapped_column(Time)

    # Relationships
    trip: Mapped["Trip"] = relationship(back_populates="preferences")

    children_age_groups: Mapped[list["ChildrenAgeGroup"]] = relationship(
        back_populates="trip_preference"
    )