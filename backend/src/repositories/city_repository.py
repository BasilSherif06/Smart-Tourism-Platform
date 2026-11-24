from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.city import City
from src.schemas.city import CityCreate


def create_city(db: Session, city: CityCreate):
    db_city = City(
        name=city.name,
        description=city.description,
        latitude=city.latitude,
        longitude=city.longitude,
        minimum_budget=city.minimum_budget
    )

    db.add(db_city)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_city)

    return db_city


def get_cities(db: Session):
    return (
        db.query(City)
        .order_by(City.city_id)
        .all()
    )


def get_city_by_id(db: Session, city_id: int):
    return (
        db.query(City)
        .filter(City.city_id == city_id)
        .first()
    )


def update_city(db: Session, city_id: int, city: CityCreate):
    db_city = get_city_by_id(db, city_id)

    if db_city is None:
        return None

    db_city.name = city.name
    db_city.description = city.description
    db_city.latitude = city.latitude
    db_city.longitude = city.longitude
    db_city.minimum_budget = city.minimum_budget

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(db_city)

    return db_city


def delete_city(db: Session, city_id: int):
    db_city = get_city_by_id(db, city_id)

    if db_city is None:
        return None

    db.delete(db_city)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    return db_city