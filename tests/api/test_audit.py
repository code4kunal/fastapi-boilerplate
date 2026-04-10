"""API test stub for module audit."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.api
async def test_audit_health(client: AsyncClient) -> None:
    r = await client.get("/api/v1/audit/health")
    assert r.status_code == 200