from fastapi import FastAPI

from src.routes.place_ticket_prices import router as place_ticket_prices_router
from src.routes.places import router as places_router
from src.routes.cities import router as cities_router

app = FastAPI(
    title="Smart Tourism Platform API",
    description="Backend API for the Smart Tourism Platform",
    version="1.0.0"
)

app.include_router(
    place_ticket_prices_router,
    prefix="/api/v1"
)

app.include_router(
    places_router,
    prefix="/api/v1"
)

app.include_router(
    cities_router,
    prefix="/api/v1"
)