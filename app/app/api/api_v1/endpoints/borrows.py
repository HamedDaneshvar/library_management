from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


status_router = APIRouter(prefix="/status", tags=["borrow status"])
user_borrow_router = APIRouter(prefix="/user", tags=["user borrow"])
namespace = "borrow"


@status_router.get("/")
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
        is_deleted=False,
    )
    return APIResponse(status)


@status_router.get("/{id}")
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
    if not status or status.is_deleted:
        raise HTTPException(status_code=404, detail="Status not found")

    return APIResponse(status)


@status_router.post("/")
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


@status_router.put("/{id}")
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

    if not status_in or status_in.is_deleted:
        raise HTTPException(status_code=404, detail="Status not found")

    if request.title is not None:
        status_in.title = request.title

    status = await crud.status.update(db, db_obj=status_in)
    return APIResponse(status)


@status_router.delete("/{id}")
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

    if not status_in or status_in.is_deleted:
        raise HTTPException(status_code=404, detail="Status not found")

    status = await crud.status.remove(db, id=id)

    return APIResponse(status)


async def find_book(db: AsyncSession, book_id: int) -> models.Book:
    book = await crud.book.get(db, id=book_id)
    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def check_book_for_borrow(book: models.Book):
    if book.borrow_qty < 1:
        raise HTTPException(status_code=404,
                            detail="Book is not available for borrow")


async def create_activity_log(
    db: AsyncSession,
    borrow_id: int,
    status_id: int
) -> None:
    activity_log_obj = schemas.BorrowActivityLogCreate(
        borrow_id=borrow_id,
        status_id=status_id
    )

    await crud.borrow_activity_log.create(
        db,
        obj_in=activity_log_obj
    )


@user_borrow_router.get("/request")
async def create_borrow_request(
    book_id: int,
    borrow_days: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Request to borrow a book
    """

    if current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book = await find_book(db, book_id)

    # step 1: insert this request into borrow table and activity log
    status_id = 1
    borrow_obj = schemas.BorrowCreate(
        book_id=book.id,
        user_id=current_user.id,
        status_id=1
    )
    # create borrow request
    borrow = await crud.borrow.create(db, obj_in=borrow_obj)
    await create_activity_log(db, borrow.id, status_id)

    await check_book_for_borrow(book)

    # step 2: if user has pending borrows is rejected
    status_id = 2
    has_pending = await crud.borrow.has_pending_borrows(db, current_user.id)
    if has_pending:
        # update borrow record
        borrow_update = schemas.BorrowUpdate(
            status_id=status_id
        )
        borrow = await crud.borrow.update(db, db_obj=borrow,
                                          obj_in=borrow_update)
        # create new activity log record
        await create_activity_log(db, borrow.id, status_id)

    # step 3: Checking the balance of the user who has enough balance
    # to borrow this book for 3 days

    return {"message": "user borrow request"}


@user_borrow_router.get("/test-query")
async def test_borrow_request(
    db: AsyncSession = Depends(deps.get_db_async),
):
    status = await crud.borrow.has_pending_borrows(db, user_id=2)
    print(status)
