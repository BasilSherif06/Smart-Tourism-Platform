from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.place_ticket_price import PlaceTicketPrice
from src.schemas.place_ticket_price import PlaceTicketPriceCreate


def create_ticket_price(
    db: Session,
    place_id: int,
    ticket_price: PlaceTicketPriceCreate
):
    db_ticket_price = PlaceTicketPrice(
        place_id=place_id,
        visitor_category=ticket_price.visitor_category,
        price_amount=ticket_price.price_amount,
        source_name=ticket_price.source_name,
        source_url=str(ticket_price.source_url),
        last_verified_at=ticket_price.last_verified_at
    )

    db.add(db_ticket_price)
    db.commit()
    db.refresh(db_ticket_price)

    return db_ticket_price


def get_ticket_prices_by_place(db: Session, place_id: int):
    return (
        db.query(PlaceTicketPrice)
        .filter(PlaceTicketPrice.place_id == place_id)
        .all()
    )


def get_ticket_price_by_id(db: Session, ticket_price_id: int):
    return db.query(PlaceTicketPrice).filter(
        PlaceTicketPrice.ticket_price_id == ticket_price_id
    ).first()


def update_ticket_price(
    db: Session,
    ticket_price_id: int,
    ticket_price: PlaceTicketPriceCreate
):
    db_ticket_price = get_ticket_price_by_id(db, ticket_price_id)

    if db_ticket_price is None:
        return None

    db_ticket_price.visitor_category = ticket_price.visitor_category
    db_ticket_price.price_amount = ticket_price.price_amount
    db_ticket_price.source_name = ticket_price.source_name
    db_ticket_price.source_url = str(ticket_price.source_url)
    db_ticket_price.last_verified_at = ticket_price.last_verified_at

    db.commit()
    db.refresh(db_ticket_price)

    return db_ticket_price


def delete_ticket_price(db: Session, ticket_price_id: int):
    db_ticket_price = get_ticket_price_by_id(db, ticket_price_id)

    if db_ticket_price is None:
        return None

    db.delete(db_ticket_price)
    db.commit()

    return db_ticket_price