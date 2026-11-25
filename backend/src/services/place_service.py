from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.repositories import city_repository, place_repository
from src.schemas.place import PlaceCreate


def _ensure_city_exists(db: Session, city_id: int):
    if city_repository.get_city_by_id(db, city_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )


def _ensure_google_place_id_is_free(
    db: Session,
    google_place_id: str,
    place_id: Optional[int] = None
):
    existing = place_repository.get_place_by_google_place_id(
        db, google_place_id
    )

    if existing is not None and existing.place_id != place_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A place with this google_place_id already exists"
        )


def create_place(db: Session, place: PlaceCreate):
    _ensure_city_exists(db, place.city_id)
    _ensure_google_place_id_is_free(db, place.google_place_id)

    try:
        return place_repository.create_place(db, place)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place conflicts with existing data"
        )


def get_places(
    db: Session,
    city_id: Optional[int] = None,
    category: Optional[str] = None
):
    return place_repository.get_places(db, city_id, category)


def get_place_by_id(db: Session, place_id: int):
    return place_repository.get_place_by_id(db, place_id)


def update_place(db: Session, place_id: int, place: PlaceCreate):
    if place_repository.get_place_by_id(db, place_id) is None:
        return None

    _ensure_city_exists(db, place.city_id)
    _ensure_google_place_id_is_free(db, place.google_place_id, place_id)

    try:
        return place_repository.update_place(db, place_id, place)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place conflicts with existing data"
        )


def delete_place(db: Session, place_id: int):
    try:
        return place_repository.delete_place(db, place_id)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Place cannot be deleted because other records depend on it"
        )