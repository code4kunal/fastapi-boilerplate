"""Sample module router."""

from __future__ import annotations

from fastapi import APIRouter

from siteops_platform.core.responses import ok

router = APIRouter()


@router.get("/health")
async def health() -> dict:
    return ok({"module": "users", "status": "ok"})