from db.migrations.create_concept_version_architecture import run as run_concept_migration
from app.concepts.routes import router as concepts_router
from app.events.routes import router as events_router
from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.diagnostic.routes import router as diagnostic_router

app = FastAPI(
    title="2FUN Platform API",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    run_concept_migration()

app.include_router(auth_router)
app.include_router(events_router)
app.include_router(diagnostic_router)
app.include_router(concepts_router)

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
