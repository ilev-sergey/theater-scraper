from fastapi import APIRouter

router = APIRouter(
    prefix="/stages",
    tags=["stages"],
    responses={404: {"description": "Not found"}},
)
