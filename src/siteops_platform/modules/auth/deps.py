"""Auth dependencies: bearer token, roles, permissions hook."""

from __future__ import annotations

from typing import Annotated, Any, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from siteops_platform.core.exceptions import AppError
from siteops_platform.modules.auth.schemas import UserClaims
from siteops_platform.modules.auth.token_service import decode_access

security = HTTPBearer(auto_error=False)


async def get_token_payload(
    creds: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)],
) -> dict[str, Any]:
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing bearer token")
    try:
        return await decode_access(creds.credentials)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


async def get_current_user(payload: Annotated[dict, Depends(get_token_payload)]) -> UserClaims:
    sub = str(payload.get("sub") or "")
    roles = list(payload.get("roles") or [])
    return UserClaims(sub=sub, roles=roles)


def require_roles(*allowed: str):
    async def _dep(user: Annotated[UserClaims, Depends(get_current_user)]) -> UserClaims:
        if allowed and not (set(allowed) & set(user.roles)) and "admin" not in user.roles:
            raise AppError("forbidden", "Insufficient role", status_code=403)
        return user

    return _dep