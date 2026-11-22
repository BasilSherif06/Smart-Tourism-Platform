from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class Place(Base):
    __tablename__ = "places"

    place_id: Mapped[int] = mapped_column(primary_key=True)
    google_place_id: Mapped[str] = mapped_column(String(255), unique=True)
    display_name: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.city_id"))
    latitude: Mapped[float]
    longitude: Mapped[float]
    address: Mapped[Optional[str]] = mapped_column(Text)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    opening_hours: Mapped[Optional[dict]] = mapped_column(JSON)
    rating: Mapped[Optional[float]] = mapped_column(Numeric(2, 1))
    good_for_children: Mapped[bool] = mapped_column(Boolean, default=False)
    good_for_groups: Mapped[bool] = mapped_column(Boolean, default=False)
    website_url: Mapped[Optional[str]] = mapped_column(String(500))
    estimated_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    indoor_outdoor: Mapped[Optional[str]] = mapped_column(String(20))
    weather_sensitivity: Mapped[Optional[str]] = mapped_column(String(20))