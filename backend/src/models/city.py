from decimal import Decimal
from typing import Optional

from sqlalchemy import Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class City(Base):
    __tablename__ = "cities"

    city_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    latitude: Mapped[float]
    longitude: Mapped[float]
    minimum_budget: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2))  # EGP