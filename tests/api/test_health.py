"""API routing contracts for health endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.api
async def test_live(client: AsyncClient) -> None:
    r = await client.get("/api/v1/health/live")
    assert r.status_code == 200
    body = r.json()
    assert body["data"]["status"] == "ok"


@pytest.mark.api
async def test_ready(client: AsyncClient) -> None:
    r = await client.get("/api/v1/health/ready")
    assert r.status_code == 200