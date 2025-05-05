from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from ..db import engine
from ..models import Performance, TheaterName
from ..services.performance_service import PerformanceService

router = APIRouter(
    prefix="/performances",
    tags=["performances"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_performances(
    theater_name: TheaterName | None = None,
) -> list[Performance]:
    """
    Get all performances or filter by theater name if provided.
    """
    with Session(engine) as session:
        service = PerformanceService()
        if theater_name:
            return service.get_by_theater_name(session, theater_name)
        else:
            return service.get_all(session)


@router.get("/{performance_id}")
async def get_performance_by_id(performance_id: int) -> Performance:
    """
    Get performance by ID.
    """
    with Session(engine) as session:
        service = PerformanceService()
        performance = service.get_by_id(session, performance_id)
        if performance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Performance with ID {performance_id} not found",
            )
        return performance
