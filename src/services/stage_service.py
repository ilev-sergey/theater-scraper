from sqlmodel import Session, select

from ..models import Stage, Theater, TheaterName
from .service import Service


class StageService(Service[Stage]):
    """Service for handling stage-related database operations"""

    def __init__(self):
        super().__init__(Stage)

    def _get_id_field(self):
        """Override to use stage_id instead of id"""
        return Stage.stage_id

    def get_by_theater_name(
        self,
        session: Session,
        theater_name: TheaterName,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Stage]:
        """
        Get objects filtered by theater name.

        Args:
            session: SQLModel database session
            theater_name: Name of the theater to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of objects matching the theater name
        """
        query = (
            select(Stage)
            .join(Stage.theater)
            .where(Theater.name == theater_name)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(query).all()

    def get_stage_id_by_name(
        self,
        session: Session,
        stage_name: str,
    ) -> int | None:
        """
        Get stage ID by stage name.

        Args:
            session: SQLModel database session
            stage_name: Name of the stage to look up

        Returns:
            Stage ID if found, None otherwise
        """
        query = select(Stage.stage_id).where(Stage.name == stage_name)
        return session.exec(query).first()
