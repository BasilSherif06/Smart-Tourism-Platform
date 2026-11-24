from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.controllers.place_controller import (
    create_place,
    delete_place,
    get_city_by_id,
    get_place_by_google_place_id,
    get_place_by_id,
    get_places,
    update_place,
)
from src.database.connection import get_db
from src.schemas.place import PlaceCreate, PlaceResponse


router = APIRouter(
    prefix="/places",
    tags=["Places"]
)


@router.post(
    "/",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_place_endpoint(
    place: PlaceCreate,
    db: Session = Depends(get_db)
):
    if get_city_by_id(db, place.city_id) is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    if get_place_by_google_place_id(db, place.google_place_id) is not None:
        raise HTTPException(
            status_code=409,
            detail="A place with this google_place_id already exists"
        )

    return create_place(db, place)


@router.get(
    "/",
    response_model=list[PlaceResponse]
)
def get_places_endpoint(
    city_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_places(db, city_id)


@router.get(
    "/{place_id}",
    response_model=PlaceResponse
)
def get_place_endpoint(
    place_id: int,
    db: Session = Depends(get_db)
):
    db_place = get_place_by_id(db, place_id)

    if db_place is None:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    return db_place


@router.put(
    "/{place_id}",
    response_model=PlaceResponse
)
def update_place_endpoint(
    place_id: int,
    place: PlaceCreate,
    db: Session = Depends(get_db)
):
    if get_place_by_id(db, place_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )

    if get_city_by_id(db, place.city_id) is None:
        raise HTTPException(
            status_code=404,
            detail="City not found"
        )

    existing = get_place_by_google_place_id(db, place.google_place_id)

    if existing is not None and existing.place_id != place_id:
        raise HTTPException(
            status_code=409,
            detail="A place with this google_place_id already exists"
        )

    return update_place(db, place_id, place)


@router.delete(
    "/{place_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_place_endpoint(
    place_id: int,
    db: Session = Depends(get_db)
):
    try:
        db_place = delete_place(db, place_id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Place cannot be deleted because other records depend on it"
        )

    if db_place is None:
        raise HTTPException(
            status_code=404,
            detail="Place not found"
        )