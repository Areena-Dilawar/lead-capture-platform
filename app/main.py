from fastapi import FastAPI

app = FastAPI(
    title="FlyRank Lead-Capture Platform",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}