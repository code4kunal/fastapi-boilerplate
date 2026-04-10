"""Idempotency-Key handling hook (plug cache or DB store)."""

from __future__ import annotations

from typing import Any, Optional


class IdempotencyStore:
    """Replace with Redis/DB for production."""

    async def seen(self, key: str) -> Optional[Any]:
        return None

    async def remember(self, key: str, response: Any) -> None:
        return None