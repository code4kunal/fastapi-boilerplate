"""Token revocation interface (swap for Redis/DB)."""

from __future__ import annotations

from typing import Protocol


class TokenRevocationStore(Protocol):
    async def is_revoked(self, jti: str) -> bool: ...
    async def revoke(self, jti: str) -> None: ...


class InMemoryRevocationStore:
    def __init__(self) -> None:
        self._jtis: set[str] = set()

    async def is_revoked(self, jti: str) -> bool:
        return jti in self._jtis

    async def revoke(self, jti: str) -> None:
        self._jtis.add(jti)