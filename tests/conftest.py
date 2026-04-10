"""Shared fixtures: in-memory SQLite, schema, HTTP client."""

from __future__ import annotations

import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("APP_ENV", "test")

from siteops_platform.core.config import get_settings
from siteops_platform.infrastructure.persistence.base import Base
from siteops_platform.infrastructure.persistence.session import dispose_engine, get_engine
from siteops_platform.main import app

get_settings.cache_clear()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _engine_and_schema() -> None:
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await dispose_engine()


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac