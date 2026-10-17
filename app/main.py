
from fastapi import FastAPI

from app.api.routes import health

app = FastAPI(
    title="Embeddable Widget & Lead-Capture Platform",
    version="0.0.1",
)

app.include_router(health.router)