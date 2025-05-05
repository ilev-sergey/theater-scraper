import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class TheaterName(str, Enum):
    ramt = "ramt"
    fomenki = "fomenki"
    sti = "sti"


class Theater(SQLModel, table=True):
    theater_id: int | None = Field(default=None, primary_key=True)
    name: TheaterName
    full_name: str | None = None
    url: str | None = None


class Stage(SQLModel, table=True):
    stage_id: int | None = Field(default=None, primary_key=True)
    name: str
    theater_id: int
    address: str | None = None


class Performance(SQLModel, table=True):
    performance_id: int | None = Field(default=None, primary_key=True)
    title: str
    stage_id: int
    datetime: datetime.datetime
    director: str | None = None
    author: str | None = None
