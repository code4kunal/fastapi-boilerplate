"""Application layer unit tests (no FastAPI)."""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock

import pytest

from siteops_platform.application.use_cases.items import CreateItemUseCase, ListItemsUseCase
from siteops_platform.core.exceptions import ValidationAppError
from siteops_platform.domain.entities.item import Item


@pytest.mark.unit
async def test_create_item_rejects_blank_name() -> None:
    repo = AsyncMock()
    uc = CreateItemUseCase(repo)
    with pytest.raises(ValidationAppError):
        await uc.execute("   ")
    repo.add.assert_not_called()


@pytest.mark.unit
async def test_list_items_returns_total() -> None:
    repo = AsyncMock()
    repo.list_page = AsyncMock(return_value=[Item(id=uuid.uuid4(), name="a")])
    repo.count = AsyncMock(return_value=1)
    uc = ListItemsUseCase(repo)
    rows, total = await uc.execute(limit=10, offset=0)
    assert total == 1
    assert len(rows) == 1