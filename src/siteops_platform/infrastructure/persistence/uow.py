"""Unit of Work: groups repositories for one transactional boundary."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from siteops_platform.infrastructure.persistence.repositories.item_repository import SqlAlchemyItemRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.items = SqlAlchemyItemRepository(session)