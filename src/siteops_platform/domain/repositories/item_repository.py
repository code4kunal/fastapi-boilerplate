"""Repository contract (dependency inversion)."""

from __future__ import annotations

import uuid
from typing import Optional, Protocol

from siteops_platform.domain.entities.item import Item


class ItemRepository(Protocol):
    async def add(self, item: Item) -> Item: ...
    async def get(self, item_id: uuid.UUID) -> Optional[Item]: ...
    async def list_page(self, *, limit: int, offset: int) -> list[Item]: ...
    async def count(self) -> int: ...