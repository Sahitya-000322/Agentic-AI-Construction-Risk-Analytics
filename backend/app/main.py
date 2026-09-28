import logging
import time
from collections.abc import Awaitable, Callable
from contextlib import asynccontextmanager
from app.routers import workers
from app.routers import attendance
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError, OperationalError
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.limiter import limiter
from app.models import (
    KPI,
    AIInsight,
    AIModule,
    AISiteStatus,
    Alert,
    Hazard,
    Incident,
    Milestone,
    PerformanceMetric,
    Project,
    Recommendation,
    Report,
    RiskSummary,
    RiskTrend,
    User,
    Zone,
)
from app.routers import (
    aihub,
    alerts,
    auth,
    dashboard,
    hazards,
    milestones,
    ml,
    ppe,
    projects,
    recommendations,
    reports,
    risks,
    zones,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("buildai")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up — creating database tables if needed...")
    Base.metadata.create_all(bind=engine)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except OperationalError:
        db_status = "DISCONNECTED"
    logger.info("Database: %s", db_status)
    logger.info("Registered %d routes", len(app.routes))
    yield
    logger.info("Shutting down.")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        if request.url.path in ("/health", "/health/detailed"):
            return await call_next(request)
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s -> %d (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


app = FastAPI(
    title="Agentic AI Construction Risk Analytics API",
    description="Backend API for the BuildAI Construction Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
    max_age=600,
)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(ml.router)
app.include_router(ppe.router)
app.include_router(projects.router)
app.include_router(milestones.router)
app.include_router(alerts.router)
app.include_router(recommendations.router)
app.include_router(hazards.router)
app.include_router(zones.router)
app.include_router(risks.router)
app.include_router(aihub.router)
app.include_router(reports.router)
app.include_router(workers.router)
app.include_router(attendance.router)

@app.exception_handler(OperationalError)
async def db_error_handler(request: Request, exc: OperationalError):
    logger.error("DB error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Database temporarily unavailable. Please retry shortly."},
    )


@app.exception_handler(DBAPIError)
async def dbapi_error_handler(request: Request, exc: DBAPIError):
    logger.error("DB API error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Database error. Please retry shortly."},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Endpoint not found: {request.method} {request.url.path}"},
    )


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


@app.get("/health/detailed", tags=["system"])
def health_detailed():
    db_ok = False
    db_error: str | None = None
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_ok = True
    except OperationalError as e:
        db_error = str(e)

    counts: dict[str, int] = {}
    if db_ok:
        db = SessionLocal()
        try:
            for model in [
                User, Project, Milestone, KPI, RiskSummary, Incident, Alert,
                Recommendation, RiskTrend, AISiteStatus, AIModule, AIInsight,
                Hazard, Zone, Report, PerformanceMetric,
            ]:
                try:
                    counts[model.__tablename__] = db.query(model).count()
                except Exception as e:  # noqa: BLE001 — per-table best effort
                    counts[model.__tablename__] = -1
                    logger.warning("count failed for %s: %s", model.__tablename__, e)
        finally:
            db.close()

    return {
        "status": "ok" if db_ok else "degraded",
        "db": "connected" if db_ok else "disconnected",
        "db_error": db_error,
        "tables": counts,
    }


# NOTE: catch-all MUST be registered last — FastAPI matches routes in order.
@app.api_route(
    "/{full_path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    include_in_schema=False,
)
async def catch_all(full_path: str, request: Request):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Endpoint not found: {request.method} /{full_path}"},
    )
