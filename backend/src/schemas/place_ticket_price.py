from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class PlaceTicketPriceCreate(BaseModel):
    visitor_category: str = Field(min_length=1, max_length=50)
    price_amount: Decimal = Field(ge=0)
    source_name: str = Field(min_length=1, max_length=150)
    source_url: HttpUrl
    last_verified_at: datetime


class PlaceTicketPriceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticket_price_id: int
    place_id: int
    visitor_category: str
    price_amount: Decimal
    source_name: str
    source_url: str
    last_verified_at: datetime