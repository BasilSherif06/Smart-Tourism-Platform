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
    category: Optional[str] = Field(default=None, max_length=100)
    opening_hours: Optional[dict] = None
    rating: Optional[Decimal] = Field(default=None, ge=0, le=5, decimal_places=1)
    good_for_children: bool = False
    good_for_groups: bool = False
    website_url: Optional[HttpUrl] = None
    estimated_duration_minutes: Optional[int] = Field(default=None, gt=0)
    indoor_outdoor: Optional[str] = Field(default=None, max_length=20)
    weather_sensitivity: Optional[str] = Field(default=None, max_length=20)


class PlaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    place_id: int
    google_place_id: str
    display_name: str
    city_id: int
    latitude: float
    longitude: float
    address: Optional[str]
    category: Optional[str]
    opening_hours: Optional[dict]
    rating: Optional[Decimal]
    good_for_children: bool
    good_for_groups: bool
    website_url: Optional[str]
    estimated_duration_minutes: Optional[int]
    indoor_outdoor: Optional[str]
    weather_sensitivity: Optional[str]