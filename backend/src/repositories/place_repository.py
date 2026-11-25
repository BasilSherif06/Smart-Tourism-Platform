from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.place import Place
from src.schemas.place import PlaceCreate


def _place_data(place: PlaceCreate) -> dict:
    data = place.model_dump()

    if data["website_url"] is not None:
        data["website_url"] = str(data["website_url"])

    return data


def get_place_by_id(db: Session, place_id: int):
    return (
        db.query(Place)
        .filter(Place.place_id == place_id)
        .first()
    )


def get_place_by_google_place_id(db: Session, google_place_id: str):
    return (
        db.query(Place)
        .filter(Place.google_place_id == google_place_id)
        .first()
    )


def get_places(
    db: Session,
    city_id: Optional[int] = None,
    category: Optional[str] = None
):
    query = db.query(Place)

    if city_id is not None:
        query = query.filter(Place.city_id == city_id)

    if category is not None:
        query = query.filter(Place.category == category)

    return query.order_by(Place.place_id).all()


def create_place(db: Session, place: PlaceCreate):
    db_place = Place(**_place_data(place))

    db.add(db_place)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_place)

    return db_place


def update_place(db: Session, place_id: int, place: PlaceCreate):
    db_place = get_place_by_id(db, place_id)

    if db_place is None:
        return None

    for field, value in _place_data(place).items():
        setattr(db_place, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_place)

    return db_place


def delete_place(db: Session, place_id: int):
    db_place = get_place_by_id(db, place_id)

    if db_place is None:
        return None

    db.delete(db_place)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return db_place