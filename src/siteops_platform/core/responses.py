"""Consistent API response envelope and exception translation."""

from __future__ import annotations

from typing import Any, Optional

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from siteops_platform.core.exceptions import AppError


def ok(data: Any = None, meta: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    body: dict[str, Any] = {"data": data, "errors": []}
    if meta is not None:
        body["meta"] = meta
    return body


async def envelope_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    correlation_id = getattr(request.state, "correlation_id", None)
    if isinstance(exc, AppError):
        payload = {
            "data": None,
            "errors": [{"code": exc.code, "message": exc.message}],
            "meta": {"correlation_id": correlation_id},
        }
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(payload))
    if isinstance(exc, RequestValidationError):
        payload = {
            "data": None,
            "errors": [{"code": "validation_error", "message": e.get("msg")} for e in exc.errors()],
            "meta": {"correlation_id": correlation_id},
        }
        return JSONResponse(status_code=422, content=jsonable_encoder(payload))
    if isinstance(exc, StarletteHTTPException):
        payload = {
            "data": None,
            "errors": [{"code": "http_error", "message": exc.detail}],
            "meta": {"correlation_id": correlation_id},
        }
        return JSONResponse(status_code=exc.status_code, content=jsonable_encoder(payload))
    payload = {
        "data": None,
        "errors": [{"code": "internal_error", "message": "Internal server error"}],
        "meta": {"correlation_id": correlation_id},
    }
    return JSONResponse(status_code=500, content=jsonable_encoder(payload))