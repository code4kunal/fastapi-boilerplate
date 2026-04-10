"""Items CRUD (sample module)."""

from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from siteops_platform.api.deps import get_uow
from siteops_platform.application.dto.pagination import PaginatedMeta, PaginationParams
from siteops_platform.application.use_cases.items import CreateItemUseCase, ListItemsUseCase
from siteops_platform.core.exceptions import NotFoundError
from siteops_platform.core.responses import ok
from siteops_platform.infrastructure.persistence.uow import UnitOfWork

router = APIRouter(prefix="/items", tags=["items"])


class ItemCreateBody(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class ItemOut(BaseModel):
    id: UUID
    name: str

    model_config = {"from_attributes": True}


@router.post("")
async def create_item(
    body: ItemCreateBody,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> dict:
    item_repository = uow.items
    create_item_use_case = CreateItemUseCase(item_repository)
    entity = await create_item_use_case.execute(body.name)
    return ok(ItemOut(id=entity.id, name=entity.name).model_dump())


@router.get("")
async def list_items(
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    page: Annotated[PaginationParams, Depends()],
) -> dict:
    item_repository = uow.items
    list_items_use_case = ListItemsUseCase(item_repository)
    rows, total = await list_items_use_case.execute(
        limit=page.limit, offset=page.offset
    )
    data = [ItemOut(id=r.id, name=r.name).model_dump() for r in rows]
    meta = PaginatedMeta(total=total, limit=page.limit, offset=page.offset).model_dump()
    return ok(data, meta=meta)


@router.get("/{item_id}")
async def get_item(
    item_id: UUID,
    uow: Annotated[UnitOfWork, Depends(get_uow)],
) -> dict:
    item_repository = uow.items
    row = await item_repository.get(item_id)
    if row is None:
        raise NotFoundError("item not found")
    return ok(ItemOut(id=row.id, name=row.name).model_dump())