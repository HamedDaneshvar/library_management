from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


router = APIRouter()
namespace = "category"


@router.get("/")
async def get_categories(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve categories.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    categories = await crud.category.filter(
        db,
        skip=skip,
        limit=limit,
        is_deleted=False
    )
    return APIResponse(categories)


@router.post("/")
async def create_category(
    category_in: schemas.CategoryCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create a new category
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    category = await crud.category.create(db, obj_in=category_in)
    return APIResponse(category)


@router.put("/{id}")
async def update_category(
    id: int,
    title: str | None = Body(None),
    borrow_limit: int | None = Body(None),
    borrow_price_per_day: int | None = Body(None),
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    update a category
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    category_in = await crud.category.get(db, id=id)

    if not category_in or category_in.is_deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    if title is not None:
        category_in.title = title
    if borrow_limit is not None:
        category_in.borrow_limit = borrow_limit
    if borrow_price_per_day is not None:
        category_in.borrow_price_per_day = borrow_price_per_day

    category = await crud.category.update(
        db,
        db_obj=category_in,
    )
    return APIResponse(category)


@router.delete("/{id}")
async def delete_category(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    delete a category
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    category_in = await crud.category.get(db, id=id)

    if not category_in or category_in.is_deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    category = await crud.category.remove(db, id=id)
    return APIResponse(category)
