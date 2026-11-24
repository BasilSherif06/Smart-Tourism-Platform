from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.connection import get_db
from src.schemas.place_ticket_price import (
    PlaceTicketPriceCreate,
    PlaceTicketPriceResponse
)
from src.services import place_ticket_price_service


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
    return place_ticket_price_service.create_ticket_price(
        db, place_id, ticket_price
    )


@router.get(
    "/",
    response_model=list[PlaceTicketPriceResponse]
)
def get_ticket_prices_endpoint(
    place_id: int,
    db: Session = Depends(get_db)
):
    return place_ticket_price_service.get_ticket_prices_by_place(
        db, place_id
    )


@router.get(
    "/ticket/{ticket_price_id}",
    response_model=PlaceTicketPriceResponse
)
def get_ticket_price_endpoint(
    ticket_price_id: int,
    db: Session = Depends(get_db)
):
    db_ticket_price = place_ticket_price_service.get_ticket_price_by_id(
        db, ticket_price_id
    )

    if db_ticket_price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    db_ticket_price = place_ticket_price_service.update_ticket_price(
        db, ticket_price_id, ticket_price
    )

    if db_ticket_price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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
    db_ticket_price = place_ticket_price_service.delete_ticket_price(
        db, ticket_price_id
    )

    if db_ticket_price is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket price not found"
        )