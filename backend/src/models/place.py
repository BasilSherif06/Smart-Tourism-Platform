from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, JSON, Numeric, String, Text
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
    category: Mapped[str] = mapped_column(String(100), index=True)
    opening_hours: Mapped[Optional[dict]] = mapped_column(JSON)
    rating: Mapped[Optional[float]] = mapped_column(Numeric(2, 1))
    good_for_children: Mapped[Optional[bool]] = mapped_column(Boolean)
    good_for_groups: Mapped[Optional[bool]] = mapped_column(Boolean)
    website_url: Mapped[Optional[str]] = mapped_column(String(500))
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))