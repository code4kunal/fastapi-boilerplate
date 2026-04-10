"""FastAPI dependencies."""

from __future__ import annotations

from typing import Annotated
from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from siteops_platform.infrastructure.persistence.session import get_session_factory
from siteops_platform.infrastructure.persistence.uow import UnitOfWork


async def get_session() -> AsyncIterator[AsyncSession]:
    async with get_session_factory()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_uow(session: Annotated[AsyncSession, Depends(get_session)]) -> UnitOfWork:
    return UnitOfWork(session)