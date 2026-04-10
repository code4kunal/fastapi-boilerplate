"""FastAPI application entry."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from siteops_platform.infrastructure.persistence.models import item as _item_model  # noqa: F401

from siteops_platform.api.v1.router import api_router
from siteops_platform.core.config import get_settings
from siteops_platform.core.exceptions import AppError
from siteops_platform.core.logging import configure_logging
from siteops_platform.core.middleware import CorrelationIdMiddleware, RequestLogMiddleware, SecurityHeadersMiddleware
from siteops_platform.core.responses import envelope_exception_handler
from siteops_platform.infrastructure.persistence.session import dispose_engine
from starlette.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

settings = get_settings()
configure_logging(settings.log_level)


def _configure_otel() -> None:
    provider = TracerProvider(
        resource=Resource.create(
            {
                "service.name": settings.otel_service_name,
            }
        )
    )
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)


_configure_otel()


@asynccontextmanager
async def lifespan(app: FastAPI):
    from siteops_platform.infrastructure.redis_client import close_redis, init_redis

    await init_redis(settings.redis_url)
    yield
    await close_redis()
    await dispose_engine()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestLogMiddleware)
    origins = (
        ["*"]
        if settings.cors_origins.strip() == "*"
        else [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    FastAPIInstrumentor.instrument_app(app)

    app.add_exception_handler(AppError, envelope_exception_handler)
    app.add_exception_handler(RequestValidationError, envelope_exception_handler)
    app.add_exception_handler(StarletteHTTPException, envelope_exception_handler)
    app.add_exception_handler(Exception, envelope_exception_handler)

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    return app


app = create_app()