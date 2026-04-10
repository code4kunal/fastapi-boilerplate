"""Item use cases (application layer)."""

from __future__ import annotations

import uuid

from siteops_platform.domain.entities.item import Item
from siteops_platform.domain.repositories.item_repository import ItemRepository


class CreateItemUseCase:
    def __init__(self, items: ItemRepository) -> None:
        self._items = items

    async def execute(self, name: str) -> Item:
        entity = Item(id=uuid.uuid4(), name=name.strip())
        if not entity.name:
            from siteops_platform.core.exceptions import ValidationAppError

            raise ValidationAppError("name required")
        return await self._items.add(entity)


class ListItemsUseCase:
    def __init__(self, items: ItemRepository) -> None:
        self._items = items

    async def execute(self, *, limit: int, offset: int) -> tuple[list[Item], int]:
        rows = await self._items.list_page(limit=limit, offset=offset)
        total = await self._items.count()
        return rows, total