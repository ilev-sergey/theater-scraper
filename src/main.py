from fastapi import FastAPI

from models import Performance, TheaterName

app = FastAPI()


@app.get("/is_alive/")
async def is_alive():
    """
    Check if the server is alive.
    """
    return {"status": "alive"}


@app.get("/performances/{performance_id}")
async def read_performance(performance_id: int) -> Performance:
    """
    Get performance by ID.
    """
    return Performance(
        performance_id=performance_id,
        title="Sample Title",
        stage_id=1,
        datetime="2023-10-01T19:00:00",
    )


@app.get("/performances/")
async def read_performances(
    theater_name: TheaterName | None = None,
) -> list[Performance]:
    """
    Get list of performances by theater name or all performances if no theater name is provided.
    """
    return [
        Performance(
            performance_id=1,
            title="Sample Title",
            stage_id=1,
            datetime="2023-10-01T19:00:00",
        )
    ]
