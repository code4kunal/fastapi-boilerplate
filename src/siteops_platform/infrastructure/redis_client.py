"""Optional Redis client (lazy connect)."""

from __future__ import annotations

from typing import Optional

import redis.asyncio as redis

_client: Optional[redis.Redis] = None


async def init_redis(url: str) -> None:
    global _client
    _client = redis.from_url(url, decode_responses=True)


async def close_redis() -> None:
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None


def get_redis() -> redis.Redis:
    if _client is None:
        msg = "Redis not initialized"
        raise RuntimeError(msg)
    return _client
