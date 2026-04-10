"""SQLAlchemy repository implementation."""

from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from siteops_platform.domain.entities.item import Item
from siteops_platform.infrastructure.persistence.models.item import ItemModel


def _to_entity(row: ItemModel) -> Item:
    return Item(id=row.id, name=row.name, created_at=row.created_at)


class SqlAlchemyItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, item: Item) -> Item:
        row = ItemModel(id=item.id, name=item.name)
        self._session.add(row)
        await self._session.flush()
        return _to_entity(row)

    async def get(self, item_id: uuid.UUID) -> Optional[Item]:
        row = await self._session.get(ItemModel, item_id)
        return _to_entity(row) if row else None

    async def list_page(self, *, limit: int, offset: int) -> list[Item]:
        stmt = select(ItemModel).order_by(ItemModel.created_at.desc()).limit(limit).offset(offset)
        rows = (await self._session.scalars(stmt)).all()
        return [_to_entity(r) for r in rows]

    async def count(self) -> int:
        stmt = select(func.count()).select_from(ItemModel)
        return int(await self._session.scalar(stmt) or 0)