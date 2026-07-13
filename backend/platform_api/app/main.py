from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI(
    title="2FUN Platform API",
    version="0.1.0"
)

app.include_router(auth_router)

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
