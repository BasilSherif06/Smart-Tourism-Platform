from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.schemas.place_ticket_price import (
    PlaceTicketPriceCreate,
    PlaceTicketPriceResponse
)
from src.controllers.place_ticket_price_controller import create_ticket_price

from src.controllers.place_ticket_price_controller import (
    create_ticket_price,
    get_ticket_prices_by_place,
    get_ticket_price_by_id,
    update_ticket_price,
    delete_ticket_price
)
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    prefix="/places/{place_id}/ticket-prices",
    tags=["Place Ticket Prices"]
)


@router.post(
    "/",
    response_model=PlaceTicketPriceResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket_price_endpoint(
    place_id: int,
    ticket_price: PlaceTicketPriceCreate,
    db: Session = Depends(get_db)
):
    return create_ticket_price(db, place_id, ticket_price)



@router.get(
    "/",
    response_model=list[PlaceTicketPriceResponse]
)
def get_ticket_prices_endpoint(
    place_id: int,
    db: Session = Depends(get_db)
):
    return get_ticket_prices_by_place(db, place_id)



@router.get(
    "/ticket/{ticket_price_id}",
    response_model=PlaceTicketPriceResponse
)
def get_ticket_price_endpoint(
    ticket_price_id: int,
    db: Session = Depends(get_db)
):
    db_ticket_price = get_ticket_price_by_id(db, ticket_price_id)

    if db_ticket_price is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket price not found"
        )

    return db_ticket_price



@router.put(
    "/ticket/{ticket_price_id}",
    response_model=PlaceTicketPriceResponse
)
def update_ticket_price_endpoint(
    ticket_price_id: int,
    ticket_price: PlaceTicketPriceCreate,
    db: Session = Depends(get_db)
):
    db_ticket_price = update_ticket_price(
        db,
        ticket_price_id,
        ticket_price
    )

    if db_ticket_price is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket price not found"
        )

    return db_ticket_price



@router.delete(
    "/ticket/{ticket_price_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ticket_price_endpoint(
    ticket_price_id: int,
    db: Session = Depends(get_db)
):
    db_ticket_price = delete_ticket_price(db, ticket_price_id)

    if db_ticket_price is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket price not found"
        )