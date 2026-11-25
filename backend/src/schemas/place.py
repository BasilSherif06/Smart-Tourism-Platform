from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class PlaceCreate(BaseModel):
    google_place_id: str = Field(min_length=1, max_length=255)
    display_name: str = Field(min_length=1, max_length=255)
    city_id: int
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address: Optional[str] = None
    category: str = Field(min_length=1, max_length=100)
    opening_hours: Optional[dict] = None
    rating: Optional[Decimal] = Field(default=None, ge=0, le=5, decimal_places=1)
    good_for_children: Optional[bool] = None
    good_for_groups: Optional[bool] = None
    website_url: Optional[HttpUrl] = None
    last_synced_at: Optional[datetime] = None


class PlaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    place_id: int
    google_place_id: str
    display_name: str
    city_id: int
    latitude: float
    longitude: float
    address: Optional[str]
    category: str
    opening_hours: Optional[dict]
    rating: Optional[Decimal]
    good_for_children: Optional[bool]
    good_for_groups: Optional[bool]
    website_url: Optional[str]
    last_synced_at: Optional[datetime]