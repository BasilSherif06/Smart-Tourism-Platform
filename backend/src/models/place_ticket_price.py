from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class PlaceTicketPrice(Base):
    __tablename__ = "place_ticket_prices"

    ticket_price_id: Mapped[int] = mapped_column(primary_key=True)

    place_id: Mapped[int] = mapped_column(
        ForeignKey("places.place_id")
    )

    visitor_category: Mapped[str] = mapped_column(String(50))

    price_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    source_name: Mapped[str] = mapped_column(String(150))

    source_url: Mapped[str] = mapped_column(String(500))

    last_verified_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    