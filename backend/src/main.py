from fastapi import FastAPI

from src.routes.place_ticket_prices import router as place_ticket_prices_router

app = FastAPI(
    title="Smart Tourism Platform API",
    description="Backend API for the Smart Tourism Platform",
    version="1.0.0"
)

app.include_router(
    place_ticket_prices_router,
    prefix="/api/v1"
)