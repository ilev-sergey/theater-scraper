import datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class TheaterName(str, Enum):
    ramt = "ramt"
    fomenki = "fomenki"
    sti = "sti"


class Theater(SQLModel, table=True):
    theater_id: int | None = Field(default=None, primary_key=True)
    name: TheaterName
    full_name: str | None = None
    url: str | None = None

    stages: list["Stage"] = Relationship(back_populates="theater")


class Stage(SQLModel, table=True):
    stage_id: int | None = Field(default=None, primary_key=True)
    name: str
    theater_id: int = Field(foreign_key="theater.theater_id")
    address: str | None = None

    theater: "Theater" = Relationship(back_populates="stages")
    performances: list["Performance"] = Relationship(back_populates="stage")


class Performance(SQLModel, table=True):
    performance_id: int | None = Field(default=None, primary_key=True)
    title: str
    stage_id: int = Field(foreign_key="stage.stage_id")
    datetime: datetime.datetime
    director: str | None = None
    author: str | None = None

    stage: "Stage" = Relationship(back_populates="performances")
