from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


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
