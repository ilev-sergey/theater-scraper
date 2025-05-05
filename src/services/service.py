from typing import Generic, Type, TypeVar

from sqlmodel import Session, SQLModel, select

from ..models import Stage, Theater, TheaterName

# Create a generic type variable bound to SQLModel
T = TypeVar("T", bound=SQLModel)


class Service(Generic[T]):
    """
    Generic base service class providing common database operations.
    """

    def __init__(self, model_class: Type[T]):
        """
        Initialize service with the model class it will work with.

        Args:
            model_class: The SQLModel class this service will handle
        """
        self.model_class = model_class

    def _get_id_field(self):
        """
        Get the ID field for the model.
        Override this in subclasses if the ID field is not named "id".
        """
        return getattr(self.model_class, "id", None)

    def get_by_id(self, session: Session, id_value: int) -> T | None:
        """
        Get an object by its ID.

        Args:
            session: SQLModel database session
            id_value: Primary key value to look up

        Returns:
            The object if found, None otherwise
        """
        # Try to use "id" as the default ID column, but allow subclasses to override
        id_field = self._get_id_field()
        query = select(self.model_class).where(id_field == id_value)
        return session.exec(query).first()

    def get_all(self, session: Session, skip: int = 0, limit: int = 100) -> list[T]:
        """
        Get all objects, with optional pagination.

        Args:
            session: SQLModel database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of objects
        """
        query = select(self.model_class).offset(skip).limit(limit)
        return session.exec(query).all()
