from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    minimum_budget: Optional[Decimal] = Field(default=None, ge=0)


class CityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city_id: int
    name: str
    description: Optional[str]
    latitude: float
    longitude: float
    minimum_budget: Optional[Decimal]