from fastapi import FastAPI

from src.core.config import settings
from src.routes import auth_routes  # new

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_routes.router)  # new


@app.get("/health")
def health_check():
    return {"status": "ok"}