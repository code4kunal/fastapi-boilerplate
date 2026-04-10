"""Liveness and readiness probes."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from siteops_platform.api.deps import get_session
from siteops_platform.core.responses import ok

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def live() -> dict:
    return ok({"status": "ok"})


@router.get("/ready")
async def ready(session: Annotated[AsyncSession, Depends(get_session)]) -> dict:
    await session.execute(text("SELECT 1"))
    return ok({"status": "ready"})