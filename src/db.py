from sqlmodel import SQLModel, create_engine

from .config import settings

engine = create_engine(settings.DATABASE_URL, echo=settings.SQL_ECHO)


def create_db_and_tables() -> None:
    """
    Create all tables defined in SQLModel classes.
    """
    SQLModel.metadata.create_all(engine)
