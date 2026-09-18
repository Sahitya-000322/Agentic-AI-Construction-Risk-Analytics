from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.config import settings
from app.database import Base, engine
from app.routers import (
    aihub,
    alerts,
    auth,
    dashboard,
    hazards,
    milestones,
    projects,
    recommendations,
    reports,
    risks,
    zones,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Agentic AI Construction Risk Analytics API",
    description="Backend API for the BuildAI Construction Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(projects.router)
app.include_router(milestones.router)
app.include_router(alerts.router)
app.include_router(recommendations.router)
app.include_router(hazards.router)
app.include_router(zones.router)
app.include_router(risks.router)
app.include_router(aihub.router)
app.include_router(reports.router)


@app.get("/", tags=["system"])
def root():
    return {"status": "ok", "message": "Agentic AI Construction Risk Analytics API"}


@app.get("/health", tags=["system"])
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except OperationalError:
        return {"status": "degraded", "db": "disconnected"}
