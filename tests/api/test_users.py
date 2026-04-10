"""API test stub for module users."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.api
async def test_users_health(client: AsyncClient) -> None:
    r = await client.get("/api/v1/users/health")
    assert r.status_code == 200