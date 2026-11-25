from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.schemas.place import PlaceCreate, PlaceResponse
from src.services import place_service


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
    return place_service.create_place(db, place)


@router.get(
    "/",
    response_model=list[PlaceResponse]
)
def get_places_endpoint(
    city_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return place_service.get_places(db, city_id, category)


@router.get(
    "/{place_id}",
    response_model=PlaceResponse
)
def get_place_endpoint(
    place_id: int,
    db: Session = Depends(get_db)
):
    db_place = place_service.get_place_by_id(db, place_id)

    if db_place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    db_place = place_service.update_place(db, place_id, place)

    if db_place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )

    return db_place


@router.delete(
    "/{place_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_place_endpoint(
    place_id: int,
    db: Session = Depends(get_db)
):
    db_place = place_service.delete_place(db, place_id)

    if db_place is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )