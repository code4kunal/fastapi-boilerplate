"""API v1 aggregate router."""

from __future__ import annotations

from fastapi import APIRouter

from siteops_platform.api.v1 import health, items
from siteops_platform.modules.auth.router import router as auth_router

# --- service_cli: module imports ---
from siteops_platform.modules.users.router import router as users_router
from siteops_platform.modules.audit.router import router as audit_router
# --- end module imports ---

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(items.router)
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

# --- service_cli: include routers ---
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(audit_router, prefix="/audit", tags=["audit"])
# --- end include routers ---