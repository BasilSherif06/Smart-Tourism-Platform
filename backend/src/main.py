from fastapi import FastAPI

from src.routes.places import router as places_router

app = FastAPI(
    title="Smart Tourism Platform API",
    description="Backend API for the Smart Tourism Platform",
    version="1.0.0"
)

app.include_router(
    places_router,
    prefix="/api/v1"
)