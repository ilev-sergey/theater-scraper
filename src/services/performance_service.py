from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from ..models import (
    Performance,
    PerformanceResponse,
    Stage,
    StageResponse,
    Theater,
    TheaterResponse,
)
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


class PerformanceResponseService:
    """Service for handling performance responses with related data"""

    def _create_performance_response(
        self, performance: Performance
    ) -> PerformanceResponse:
        """
        Convert a Performance object to a PerformanceResponse with related data.
        """
        return PerformanceResponse(
            performance_id=performance.performance_id,
            title=performance.title,
            datetime=performance.datetime,
            director=performance.director,
            author=performance.author,
            stage=StageResponse(
                stage_id=performance.stage.stage_id,
                name=performance.stage.name,
                address=performance.stage.address,
            ),
            theater=TheaterResponse(
                theater_id=performance.stage.theater.theater_id,
                full_name=performance.stage.theater.full_name,
                url=performance.stage.theater.url,
            ),
        )

    def get_by_id(
        self,
        session: Session,
        performance_id: int,
    ) -> PerformanceResponse | None:
        """
        Get a performance by ID with stage and theater data.

        Args:
            session: SQLModel database session
            performance_id: ID of the performance to retrieve

        Returns:
            Performance response with related data or None if not found
        """
        query = (
            select(Performance)
            .options(joinedload(Performance.stage).joinedload(Stage.theater))
            .where(Performance.performance_id == performance_id)
        )
        result = session.exec(query).first()

        if not result:
            return None

        return self._create_performance_response(result)

    def get_all(
        self, session: Session, skip: int = 0, limit: int = 100
    ) -> list[PerformanceResponse]:
        """
        Get all performances with stage and theater data.

        Args:
            session: SQLModel database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of performance responses with related data
        """
        query = (
            select(Performance)
            .options(joinedload(Performance.stage).joinedload(Stage.theater))
            .offset(skip)
            .limit(limit)
        )
        results = session.exec(query).all()

        return [self._create_performance_response(perf) for perf in results]

    def get_by_theater_name(
        self,
        session: Session,
        theater_name: str,
    ) -> list[PerformanceResponse]:
        """
        Get performances by theater name with stage and theater data.

        Args:
            session: SQLModel database session
            theater_name: Name of the theater to filter by

        Returns:
            List of performance responses matching the theater name
        """
        query = (
            select(Performance)
            .options(joinedload(Performance.stage).joinedload(Stage.theater))
            .join(Performance.stage)
            .join(Stage.theater)
            .where(Theater.name == theater_name)
        )
        results = session.exec(query).all()

        return [self._create_performance_response(perf) for perf in results]
