from fastapi import FastAPI

app = FastAPI()


@app.get("/is_alive/")
async def is_alive():
    return {"status": "alive"}
