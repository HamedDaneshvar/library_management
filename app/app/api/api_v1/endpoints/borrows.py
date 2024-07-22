from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


router = APIRouter()
namespace = "borrow"


@router.get("/status")
async def get_all_status(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve all status.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    status = await crud.status.filter(
        db,
        skip=skip,
        limit=limit,
    )
    return APIResponse(status)


@router.get("/status/{id}")
async def get_status(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve a status.
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    status = await crud.status.get(db, id=id)
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")

    return APIResponse(status)


@router.post("/status/")
async def create_status(
    status_in: schemas.StatusCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create a new status
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    status = await crud.status.create(db, obj_in=status_in)
    return APIResponse(status)


@router.put("/status/{id}")
async def update_status(
    id: int,
    request: schemas.StatusUpdate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    update a status
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    status_in = await crud.status.get(db, id=id)

    if not status_in:
        raise HTTPException(status_code=404, detail="Status not found")

    if request.title is not None:
        status_in.title = request.title

    status = await crud.status.update(db, db_obj=status_in)
    return APIResponse(status)


@router.delete("/status/{id}")
async def delete_status(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    delete a status
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    status_in = await crud.status.get(db, id=id)

    if not status_in:
        raise HTTPException(status_code=404, detail="Status not found")

    status = await crud.status.remove(db, id=id)

    return APIResponse(status)
