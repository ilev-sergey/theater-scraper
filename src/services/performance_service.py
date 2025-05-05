from sqlmodel import Session, select

from ..models import Performance, Stage, Theater
from .service import Service


class PerformanceService(Service[Performance]):
    """Service for handling performance-related database operations"""

    def __init__(self):
        super().__init__(Performance)

    def _get_id_field(self):
        """Override to use performance_id instead of id"""
        return Performance.performance_id

    def get_by_theater_name(
        self,
        session: Session,
        theater_name: str,
    ) -> list[Performance]:
        """
        Get objects filtered by theater name.

        Args:
            session: SQLModel database session
            theater_name: Name of the theater to filter by

        Returns:
            List of objects matching the theater name
        """
        query = (
            select(Performance)
            .join(Performance.stage)
            .join(Stage.theater)
            .where(Theater.name == theater_name)
        )
        return session.exec(query).all()
