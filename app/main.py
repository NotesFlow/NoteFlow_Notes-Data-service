from fastapi import FastAPI

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import Note  # noqa: F401
from app.routers import health, notes

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


@app.on_event('startup')
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(health.router)
app.include_router(notes.router)
