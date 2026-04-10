"""Contract-style tests: in-memory SQLite + real repository."""

from __future__ import annotations

import uuid

import pytest

from siteops_platform.domain.entities.item import Item
from siteops_platform.infrastructure.persistence.repositories.item_repository import SqlAlchemyItemRepository
from siteops_platform.infrastructure.persistence.session import get_session_factory


@pytest.mark.unit
async def test_item_repository_add_and_get() -> None:
    async with get_session_factory()() as session:
        repo = SqlAlchemyItemRepository(session)
        e = Item(id=uuid.uuid4(), name="widget")
        saved = await repo.add(e)
        await session.commit()
        got = await repo.get(saved.id)
        assert got is not None
        assert got.name == "widget"