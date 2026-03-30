"""medinovai-connector-framework — FastAPI entrypoint."""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator

import structlog
from fastapi import FastAPI, Request
from api.routes import mos_router, register_exception_handlers
from settings import get_settings

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

mos_logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Configure logging level from settings on startup."""

    mos_settings = get_settings()
    mos_logger.info(
        "startup",
        service=mos_settings.service_name,
        category="SYSTEM",
        phi_safe=True,
    )
    yield
    mos_logger.info("shutdown", category="SYSTEM", phi_safe=True)


def create_app() -> FastAPI:
    """Application factory."""

    mos_settings = get_settings()
    mos_app = FastAPI(
        title="medinovai-connector-framework",
        version="1.0.0",
        lifespan=lifespan,
    )

    @mos_app.middleware("http")
    async def mos_correlation_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        mos_cid = request.headers.get("x-correlation-id") or str(uuid.uuid4())
        request.state.mos_correlationId = mos_cid
        mos_response = await call_next(request)
        mos_response.headers["x-correlation-id"] = mos_cid
        return mos_response

    mos_app.include_router(mos_router)
    register_exception_handlers(mos_app)
    return mos_app


app = create_app()
