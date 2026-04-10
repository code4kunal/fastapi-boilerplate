"""JWT access + refresh tokens."""

from __future__ import annotations

import secrets
import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from siteops_platform.core.config import get_settings
from siteops_platform.modules.auth.revocation import InMemoryRevocationStore

settings = get_settings()
_store = InMemoryRevocationStore()


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


def create_access_token(*, sub: str, roles: list[str]) -> str:
    exp = _now() + timedelta(seconds=settings.jwt_access_ttl_seconds)
    payload = {
        "sub": sub,
        "roles": roles,
        "type": "access",
        "exp": exp,
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


def create_refresh_token(*, sub: str) -> str:
    exp = _now() + timedelta(seconds=settings.jwt_refresh_ttl_seconds)
    payload = {
        "sub": sub,
        "type": "refresh",
        "exp": exp,
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


async def decode_access(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    except JWTError as e:
        raise ValueError("invalid token") from e
    if payload.get("type") != "access":
        raise ValueError("not an access token")
    jti = str(payload.get("jti") or "")
    if jti and await _store.is_revoked(jti):
        raise ValueError("revoked")
    return payload


async def decode_refresh(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    except JWTError as e:
        raise ValueError("invalid token") from e
    if payload.get("type") != "refresh":
        raise ValueError("not a refresh token")
    return payload


async def revoke_access_jti(jti: str) -> None:
    await _store.revoke(jti)


def verify_demo_login(username: str, password: str) -> bool:
    """Demo gate; override via AUTH_DEMO_USER / AUTH_DEMO_PASS."""
    return secrets.compare_digest(username, settings.auth_demo_user) and secrets.compare_digest(
        password,
        settings.auth_demo_pass,
    )