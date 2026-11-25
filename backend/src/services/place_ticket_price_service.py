from sqlalchemy.orm import Session

from src.schemas.place_ticket_price import PlaceTicketPriceCreate
from src.repositories import place_ticket_price_repository


def create_ticket_price(
    db: Session,
    place_id: int,
    ticket_price: PlaceTicketPriceCreate   
):
    return place_ticket_price_repository.create_ticket_price(
        db, place_id, ticket_price
    )


def get_ticket_prices_by_place(db: Session, place_id: int):
    return place_ticket_price_repository.get_ticket_prices_by_place(
        db, place_id
    )


def get_ticket_price_by_id(db: Session, ticket_price_id: int):
    return place_ticket_price_repository.get_ticket_price_by_id(
        db, ticket_price_id
    )


def update_ticket_price(
    db: Session,
    ticket_price_id: int,
    ticket_price: PlaceTicketPriceCreate
):
    return place_ticket_price_repository.update_ticket_price(
        db, ticket_price_id, ticket_price
    )


def delete_ticket_price(db: Session, ticket_price_id: int):
    return place_ticket_price_repository.delete_ticket_price(
        db, ticket_price_id
    )