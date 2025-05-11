from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from ..db import engine
from ..models import Stage, Theater, TheaterName
from ..services.theater_service import TheaterService

router = APIRouter(
    prefix="/theaters",
    tags=["theaters"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_theaters() -> list[Theater]:
    """
    Get all theaters or filter by theater name if provided.
    """
    with Session(engine) as session:
        service = TheaterService()
        return service.get_all(session)


@router.get("/id/{theater_id}")
async def get_theater_by_id(theater_id: int) -> Theater:
    """
    Get theater by ID.
    """
    with Session(engine) as session:
        service = TheaterService()
        theater = service.get_by_id(session, theater_id)
        if theater is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"theater with ID {theater_id} not found",
            )
        return theater


@router.get("/name/{theater_name}")
async def get_theater_by_name(theater_name: TheaterName) -> Theater:
    """
    Get theater by name.
    """
    with Session(engine) as session:
        service = TheaterService()
        theater = service.get_by_theater_name(session, theater_name)
        if theater is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"theater with name {theater_name} not found",
            )
        return theater
