from fastapi import APIRouter, HTTPException, status
from sqlmodel import Session

from ..db import engine
from ..models import Stage, TheaterName
from ..services.stage_service import StageService

router = APIRouter(
    prefix="/stages",
    tags=["stages"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_stages(theater_name: TheaterName | None = None) -> list[Stage]:
    """
    Get all stages or filter by theater name if provided.
    """
    with Session(engine) as session:
        service = StageService()
        if theater_name:
            return service.get_by_theater_name(session, theater_name)
        else:
            return service.get_all(session)


@router.get("/{stage_id}")
async def get_stage_by_id(stage_id: int) -> Stage:
    """
    Get stage by ID.
    """
    with Session(engine) as session:
        service = StageService()
        stage = service.get_by_id(session, stage_id)
        if stage is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Stage with ID {stage_id} not found",
            )
        return stage
