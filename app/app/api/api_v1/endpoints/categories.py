from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


router = APIRouter()
namespace = "category"


def map_categories_to_schema(
    user: models.Category,
    categories: List[models.Category]
) -> Union[List[schemas.CategoryOutSuperuser] | List[schemas.CategoryOutUser]]:
    if user.is_superuser:
        return [schemas.CategoryOutSuperuser(
                title=cat.title,
                borrow_limit=cat.borrow_limit,
                borrow_price_per_day=cat.borrow_price_per_day)
                for cat in categories]
    else:
        return [schemas.CategoryOutUser(
                title=cat.title,
                borrow_price_per_day=cat.borrow_price_per_day)
                for cat in categories]


@router.get("/")
async def get_categories(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[Union[List[schemas.CategoryOutSuperuser] |
                           List[schemas.CategoryOutUser]]]:
    """
    Retrieve categories.
    """

    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=401, detail="Unauthorized access")

    categories = await crud.category.filter(
        db,
        skip=skip,
        limit=limit,
        is_deleted=False
    )
    categories = map_categories_to_schema(current_user, categories)
    return APIResponse(categories)


@router.get("/{id}/")
async def get_category(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[Union[schemas.CategoryOutSuperuser |
                           schemas.CategoryOutUser]]:
    """
    Retrieve a category.
    """

    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=401, detail="Unauthorized access")

    category = await crud.category.get(db, id=id)
    if not category or category.is_deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    category = map_categories_to_schema(current_user, [category])[0]
    return APIResponse(category)


@router.post("/")
async def create_category(
    category_in: schemas.CategoryCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[schemas.CategoryOutSuperuser]:
    """
    Create a new category
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    category = await crud.category.create(db, obj_in=category_in)
    category = map_categories_to_schema(current_user, [category])[0]
    return APIResponse(category)


@router.put("/{id}/")
async def update_category(
    id: int,
    request: schemas.CategoryUpdate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[schemas.CategoryOutSuperuser]:
    """
    update a category
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    category_in = await crud.category.get(db, id=id)

    if not category_in or category_in.is_deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    if request.title is not None:
        category_in.title = request.title
    if request.borrow_limit is not None:
        category_in.borrow_limit = request.borrow_limit
    if request.borrow_price_per_day is not None:
        category_in.borrow_price_per_day = request.borrow_price_per_day

    category = await crud.category.update(
        db,
        db_obj=category_in,
    )
    category = map_categories_to_schema(current_user, [category])[0]
    return APIResponse(category)


@router.delete("/{id}/")
async def delete_category(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponse[schemas.CategoryDelete]:
    """
    delete a category
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    category_in = await crud.category.get(db, id=id)

    if not category_in or category_in.is_deleted:
        raise HTTPException(status_code=404, detail="Category not found")

    await crud.category.remove(db, id=id)
    item = schemas.CategoryDelete()
    return APIResponse(item)
