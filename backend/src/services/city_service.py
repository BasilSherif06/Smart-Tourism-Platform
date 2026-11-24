from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.schemas.city import CityCreate
from src.repositories import city_repository


def create_city(db: Session, city: CityCreate):
    try:
        return city_repository.create_city(db, city)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A city with this name already exists"
        )


def get_cities(db: Session):
    return city_repository.get_cities(db)


def get_city_by_id(db: Session, city_id: int):
    return city_repository.get_city_by_id(db, city_id)


def update_city(db: Session, city_id: int, city: CityCreate):
    try:
        return city_repository.update_city(db, city_id, city)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A city with this name already exists"
        )


def delete_city(db: Session, city_id: int):
    try:
        return city_repository.delete_city(db, city_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="City is used by other records and cannot be deleted"
        )