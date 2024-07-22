from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


router = APIRouter()
namespace = "report"


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
