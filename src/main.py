from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session

from .api import db, performances, stages, theaters
from .db import create_db_and_tables, engine
from .db_init import seed_theaters_and_stages
from .scrapers.manager import ScraperManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for FastAPI app lifespan events.
    """
    create_db_and_tables()
    with Session(engine) as session:
        seed_theaters_and_stages(session)

    await ScraperManager.run_all_scrapers()

    yield


app = FastAPI(lifespan=lifespan)

app.include_router(db.router)
app.include_router(performances.router)
app.include_router(theaters.router)
app.include_router(stages.router)


@app.get("/is_alive/")
async def is_alive():
    """
    Check if the server is alive.
    """
    return {"status": "alive"}
