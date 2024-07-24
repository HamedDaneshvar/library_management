from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas
from .borrows import create_activity_log


router = APIRouter()
namespace = "management"


@router.get('/books-for-sale')
async def get_books_for_sale(
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[list[schemas.Book]]:
    """
    Retrieve all books for sale
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    books = await crud.book.filter(
        db,
        models.Book.sell_qty < 30,
        is_deleted=False
    )

    books = [schemas.Book.from_orm(book) for book in books]

    return APIResponse(books)


@router.get('/revenue-summary')
async def get_revenue_report_by_category(
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[List[schemas.RevenueSummary]]:
    """
    Revenue reporting service by category
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    summary = await crud.payment.get_sum_by_category(db)
    return APIResponse(summary)


@router.get("/user/{user_id}/borrows")
async def get_user_borrows(
    user_id: int,
    book_name: Optional[str] =
        Query(None, description="Filter by book name"),
    category_name: Optional[str] =
        Query(None, description="Filter by category name"),
    borrow_count: Optional[int] =
        Query(None, description="Filter by number of times borrowed"),
    borrow_qty: Optional[int] =
        Query(None, description="Filter by borrow quantity"),
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[List[schemas.Book]]:
    """
    View books borrowed by the user
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    books = await crud.borrow.get_borrowed_books_by_user(
        db,
        user_id,
        book_name=book_name,
        category_name=category_name,
        borrow_count=borrow_count,
        borrow_qty=borrow_qty
    )
    return APIResponse(books)


@router.get("/penalties")
async def get_user_penalties(
    order_by: str = "desc",
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[List[schemas.UserPenaltySummary]]:
    """
    view get user penalties
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    if order_by.lower() not in ["desc", "asc"]:
        raise HTTPException(status_code=400, detail="Invalid order_by value")

    penalties = await crud.user_penalty.get_user_penalties(db, order_by)
    return APIResponse(penalties)


@router.put("/lending-book")
async def lending_book(
    borrow_id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Lending book to user
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    borrow = crud.borrow.get(db, id=borrow_id)

    if not borrow or borrow.is_deleted:
        raise HTTPException(status_code=404, detail="Borrow record is \
                            not found")

    pending_status_id = 5
    if borrow.status_id < pending_status_id:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # step 1: lending book to user by staff
    status_id = 5  # Borrowed status
    borrow_update = schemas.BorrowUpdate(
        status_id=status_id,
        superuser_id=current_user.id
    )
    borrow = await crud.borrow.update(db, db_obj=borrow,
                                      obj_in=borrow_update)
    # create new activity log record
    await create_activity_log(db, borrow.id, status_id)

    return APIResponse({"message": "Book was lent to the user"})


@router.put("/delivered-book")
async def delivered_book(
    borrow_id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    delivere book to staff
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    borrow = crud.borrow.get(db, id=borrow_id)

    if not borrow or borrow.is_deleted:
        raise HTTPException(status_code=404, detail="Borrow record is \
                            not found")

    pending_status_id = 5
    if borrow.status_id < pending_status_id:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    # step 1: deliver book by user to staff
    # calculate borrow_price and borrow penalty price and update borrow
    status_id = 7  # Delivered status
    superuser_id = current_user.id
    borrow = crud.borrow.update_and_calculate_borrow(
        db, status_id,
        superuser_id, borrow
    )

    # create new activity log record
    await create_activity_log(db, borrow.id, status_id)

    # add penalty of user into user penalty
    now = datetime.now()
    days_penalty = (now - borrow.max_delivery_date).days \
        if now > borrow.max_delivery_date else 0

    if days_penalty:
        user_penalty_in = schemas.UserPenaltyCreate(
            user_id=borrow.user_id,
            borrow_id=borrow.id,
            borrow_penalty_day=days_penalty
        )
        user_penalty = await crud.user_penalty.create(
            db, obj_in=user_penalty_in)

    # Increase the number of books to borrow
    book = crud.book.get(id=borrow.book_id)
    book_update = schemas.BookUpdate(
        borrow_qty=book.borrow_qty + 1
    )
    book = await crud.book.update(db, db_obj=book,
                                  obj_in=book_update)

    return APIResponse({"message": "Book was delivered by the user"})
