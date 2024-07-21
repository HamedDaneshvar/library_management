from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api import deps
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
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
