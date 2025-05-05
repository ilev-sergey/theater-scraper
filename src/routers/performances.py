from fastapi import APIRouter
from sqlmodel import Session, select

from ..db import engine
from ..models import Performance, TheaterName

router = APIRouter(
    prefix="/performances",
    tags=["performances"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{performance_id}")
async def get_performance(performance_id: int) -> Performance:
    """
    Get performance by ID.
    """
    return Performance(
        performance_id=performance_id,
        title="Sample Title",
        stage_id=1,
        datetime="2023-10-01T19:00:00",
    )


@router.get("/")
async def list_performances(
    theater_name: TheaterName | None = None,
) -> list[Performance]:
    """
    Get list of performances by theater name or all performances if no theater name is provided.
    """
    with Session(engine) as session:
        return session.exec(select(Performance)).all()
