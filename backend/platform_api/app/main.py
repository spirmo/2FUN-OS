from fastapi import FastAPI

app = FastAPI(
    title="2FUN Platform API",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "2FUN Platform API"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
