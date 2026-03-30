"""FastAPI routes: health, per-connector probes, ingest, registry."""

from __future__ import annotations

import uuid
from typing import Annotated, Any, Dict, List, Literal

import structlog
from fastapi import APIRouter, Body, HTTPException, Request

from connectors.registry import get_connector_registry

mos_router = APIRouter()
mos_logger = structlog.get_logger()

PlatformSlug = Literal[
    "aws",
    "datavant",
    "trinetx",
    "n3c",
    "pcornet",
    "mayo",
    "azure",
    "all_of_us",
]


@mos_router.get("/health")
async def service_health() -> Dict[str, Any]:
    """Service liveness (Kubernetes-friendly)."""

    return {"status": "healthy", "service": "medinovai-connector-framework"}


@mos_router.get("/ready")
async def service_ready() -> Dict[str, Any]:
    """Readiness: registry built."""

    mos_reg = get_connector_registry()
    return {
        "status": "ready",
        "connectors_registered": len(mos_reg),
    }


@mos_router.get("/health/summary")
async def health_summary(request: Request) -> Dict[str, Any]:
    """Aggregate health for all connectors (no PHI)."""

    mos_correlationId = getattr(request.state, "mos_correlationId", None)
    mos_reg = get_connector_registry()
    mos_results: List[Dict[str, Any]] = []
    for mos_slug, mos_conn in mos_reg.items():
        mos_h = await mos_conn.health_check()
        mos_results.append({"slug": mos_slug, **mos_h})
    mos_logger.info(
        "health_summary",
        correlation_id=mos_correlationId,
        connector_count=len(mos_reg),
        category="SYSTEM",
        phi_safe=True,
    )
    return {"connectors": mos_results}


@mos_router.get("/health/{mos_platform}", response_model=None)
async def health_platform(
    request: Request,
    mos_platform: PlatformSlug,
) -> Dict[str, Any]:
    """Per-connector health: /health/aws, /health/datavant, etc."""

    mos_correlationId = getattr(request.state, "mos_correlationId", None)
    mos_reg = get_connector_registry()
    mos_conn = mos_reg.get(mos_platform)
    if mos_conn is None:
        raise HTTPException(status_code=404, detail="unknown_platform")
    mos_out = await mos_conn.health_check()
    mos_logger.info(
        "connector_health",
        correlation_id=mos_correlationId,
        platform=mos_platform,
        category="SYSTEM",
        phi_safe=True,
    )
    return mos_out


@mos_router.get("/connectors")
async def list_connectors() -> Dict[str, Any]:
    """Registered connectors and static metadata."""

    mos_reg = get_connector_registry()
    mos_items = [c.describe() for c in mos_reg.values()]
    return {"count": len(mos_items), "connectors": mos_items}


@mos_router.post("/ingest/{mos_platform}")
async def ingest_single(
    request: Request,
    mos_platform: PlatformSlug,
    mos_body: Annotated[Dict[str, Any], Body(default_factory=dict)],
) -> Dict[str, Any]:
    """Single-record ingest stub routed to the selected connector."""

    mos_correlationId = getattr(request.state, "mos_correlationId", None)
    mos_reg = get_connector_registry()
    mos_conn = mos_reg.get(mos_platform)
    if mos_conn is None:
        raise HTTPException(status_code=404, detail="unknown_platform")
    mos_logger.info(
        "ingest_request",
        correlation_id=mos_correlationId,
        platform=mos_platform,
        field_count=len(mos_body),
        category="business",
        phi_safe=True,
    )
    return await mos_conn.ingest(mos_body)


@mos_router.post("/ingest/batch/{mos_platform}")
async def ingest_batch(
    request: Request,
    mos_platform: PlatformSlug,
    mos_items: Annotated[List[Dict[str, Any]], Body(...)],
) -> Dict[str, Any]:
    """Batch ingest: sequential stub calls (replace with bulk SDK later)."""

    mos_correlationId = getattr(request.state, "mos_correlationId", None)
    mos_reg = get_connector_registry()
    mos_conn = mos_reg.get(mos_platform)
    if mos_conn is None:
        raise HTTPException(status_code=404, detail="unknown_platform")
    mos_results: List[Dict[str, Any]] = []
    for mos_idx, mos_row in enumerate(mos_items):
        mos_one = await mos_conn.ingest(mos_row)
        mos_results.append({"index": mos_idx, **mos_one})
    mos_logger.info(
        "ingest_batch",
        correlation_id=mos_correlationId,
        platform=mos_platform,
        batch_size=len(mos_items),
        category="business",
        phi_safe=True,
    )
    return {"platform": mos_platform, "count": len(mos_results), "results": mos_results}


def register_exception_handlers(app: Any) -> None:
    """Attach global safe error handler."""

    @app.exception_handler(Exception)
    async def mos_unhandled(exc: Exception, request: Request) -> Response:
        from fastapi.responses import JSONResponse

        mos_correlationId = getattr(request.state, "mos_correlationId", str(uuid.uuid4()))
        mos_logger.error(
            "unhandled_error",
            correlation_id=mos_correlationId,
            error_type=type(exc).__name__,
            category="SYSTEM",
            phi_safe=True,
        )
        return JSONResponse(
            status_code=500,
            content={
                "detail": "internal_error",
                "correlation_id": mos_correlationId,
            },
        )
