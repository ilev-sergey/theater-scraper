from sqlmodel import Session, select

from ..models import Theater, TheaterName
from .service import Service


class TheaterService(Service[Theater]):
    """Service for handling theater-related database operations"""

    def __init__(self):
        super().__init__(Theater)

    def _get_id_field(self):
        """Override to use theater_id instead of id"""
        return Theater.theater_id

    def get_by_theater_name(
        self,
        session: Session,
        theater_name: TheaterName,
    ) -> list[Theater]:
        """
        Get objects filtered by theater name.

        Args:
            session: SQLModel database session
            theater_name: Name of the theater to filter by

        Returns:
            List of objects matching the theater name
        """
        query = select(Theater).where(Theater.name == theater_name)
        return session.exec(query).one()
