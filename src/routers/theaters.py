from fastapi import APIRouter

router = APIRouter(
    prefix="/theaters",
    tags=["theaters"],
    responses={404: {"description": "Not found"}},
)
