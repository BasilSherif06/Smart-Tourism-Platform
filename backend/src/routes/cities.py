from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.schemas.city import CityCreate, CityResponse
from src.controllers.city_controller import (
    create_city,
    get_cities,
    get_city_by_id,
    update_city,
    delete_city
)


router = APIRouter(
    prefix="/cities",
    tags=["Cities"]
)


@router.post(
    "/",
    response_model=CityResponse,
    status_code=status.HTTP_201_CREATED
)
def create_city_endpoint(
    city: CityCreate,
    db: Session = Depends(get_db)
):
    return create_city(db, city)


@router.get(
    "/",
    response_model=list[CityResponse]
)
def get_cities_endpoint(
    db: Session = Depends(get_db)
):
    return get_cities(db)


@router.get(
    "/{city_id}",
    response_model=CityResponse
)
def get_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db)
):
    db_city = get_city_by_id(db, city_id)

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return db_city


@router.put(
    "/{city_id}",
    response_model=CityResponse
)
def update_city_endpoint(
    city_id: int,
    city: CityCreate,
    db: Session = Depends(get_db)
):
    db_city = update_city(db, city_id, city)

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return db_city


@router.delete(
    "/{city_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_city_endpoint(
    city_id: int,
    db: Session = Depends(get_db)
):
    db_city = delete_city(db, city_id)

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )