from fastapi import FastAPI

from app.api.clubs import router as clubs_router

app = FastAPI(title="TOP20 - Argentine Football Rankings")

app.include_router(clubs_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}