from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import Session

from .db import create_db_and_tables, engine
from .db_init import seed_theaters_and_stages
from .models import Performance, TheaterName


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for FastAPI app lifespan events.
    """
    create_db_and_tables()
    with Session(engine) as session:
        seed_theaters_and_stages(session)
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/is_alive/")
async def is_alive():
    """
    Check if the server is alive.
    """
    return {"status": "alive"}


@app.get("/performances/{performance_id}")
async def read_performance(performance_id: int) -> Performance:
    """
    Get performance by ID.
    """
    return Performance(
        performance_id=performance_id,
        title="Sample Title",
        stage_id=1,
        datetime="2023-10-01T19:00:00",
    )


@app.get("/performances/")
async def read_performances(
    theater_name: TheaterName | None = None,
) -> list[Performance]:
    """
    Get list of performances by theater name or all performances if no theater name is provided.
    """
    return [
        Performance(
            performance_id=1,
            title="Sample Title",
            stage_id=1,
            datetime="2023-10-01T19:00:00",
        )
    ]
