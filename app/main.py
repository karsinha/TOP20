from fastapi import FastAPI

app = FastAPI(title="TOP20 - Argentine Football Rankings")


@app.get("/health")
def health_check():
    return {"status": "ok"}