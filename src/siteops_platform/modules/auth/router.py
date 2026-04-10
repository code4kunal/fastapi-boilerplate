"""Auth routes: login, refresh, current user."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from siteops_platform.core.responses import ok
from siteops_platform.modules.auth.deps import get_current_user
from siteops_platform.modules.auth.schemas import LoginRequest, RefreshRequest, TokenPair, UserClaims
from siteops_platform.modules.auth.token_service import (
    create_access_token,
    create_refresh_token,
    decode_refresh,
    verify_demo_login,
)

router = APIRouter()


@router.post("/login", response_model=None)
async def login(body: LoginRequest) -> dict:
    if not verify_demo_login(body.username, body.password):
        from siteops_platform.core.exceptions import AppError

        raise AppError("unauthorized", "Invalid credentials", status_code=401)
    access = create_access_token(sub=body.username, roles=["user"])
    refresh = create_refresh_token(sub=body.username)
    return ok(TokenPair(access_token=access, refresh_token=refresh).model_dump())


@router.post("/refresh", response_model=None)
async def refresh(body: RefreshRequest) -> dict:
    try:
        payload = await decode_refresh(body.refresh_token)
    except ValueError:
        from siteops_platform.core.exceptions import AppError

        raise AppError("unauthorized", "Invalid refresh token", status_code=401)
    sub = str(payload.get("sub") or "")
    access = create_access_token(sub=sub, roles=["user"])
    new_refresh = create_refresh_token(sub=sub)
    return ok(TokenPair(access_token=access, refresh_token=new_refresh).model_dump())


@router.get("/me", response_model=None)
async def me(user: Annotated[UserClaims, Depends(get_current_user)]) -> dict:
    return ok(user.model_dump())