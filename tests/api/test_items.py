"""Items API smoke tests."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.api
async def test_create_and_list_items(client: AsyncClient) -> None:
    r = await client.post("/api/v1/items", json={"name": "hello"})
    assert r.status_code == 200
    item_id = r.json()["data"]["id"]
    r2 = await client.get("/api/v1/items")
    assert r2.status_code == 200
    assert any(row["id"] == item_id for row in r2.json()["data"])