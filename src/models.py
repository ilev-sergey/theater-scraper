import datetime
from enum import Enum

from pydantic import BaseModel


class TheaterName(str, Enum):
    ramt = "ramt"
    fomenki = "fomenki"
    sti = "sti"


class Theater(BaseModel):
    theater_id: int
    name: TheaterName
    full_name: str | None = None
    url: str | None = None


class Stage(BaseModel):
    stage_id: int
    name: str
    theater_id: int
    address: str | None = None


class Performance(BaseModel):
    performance_id: int
    title: str
    stage_id: int
    datetime: datetime.datetime
    director: str | None = None
    author: str | None = None
