from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class ChildrenAgeGroup(Base):
    __tablename__ = "children_age_groups"

    child_age_group_id: Mapped[int] = mapped_column(primary_key=True)

    trip_preference_id: Mapped[int] = mapped_column(
        ForeignKey("trip_preferences.trip_preference_id")
    )

    age_group: Mapped[str] = mapped_column(String(50))

    # Relationships
    trip_preference: Mapped["TripPreference"] = relationship(
        back_populates="children_age_groups"
    )