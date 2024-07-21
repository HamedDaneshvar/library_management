from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


router = APIRouter()
namespace = "book"


@router.get("/")
async def get_books(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve books.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    books = await crud.book.filter(
        db,
        skip=skip,
        limit=limit,
        is_deleted=False
    )
    return APIResponse(books)


@router.get("/{id}")
async def get_book(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve a book.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book = await crud.book.get(db, id=id)
    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    return APIResponse(book)


@router.post("/")
async def create_book(
    book_in: schemas.BookCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create a new book
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    category_id = book_in.category_id
    category = await crud.category.get(db, id=category_id)

    if category is None:
        raise HTTPException(status_code=422, detail=f"Category with {category_id} id does not exist")

    book = await crud.book.create(db, obj_in=book_in)
    return APIResponse(book)


@router.put("/{id}")
async def update_book(
    id: int,
    title: str | None = Body(None),
    category_id: int | None = Body(None),
    borrow_qty: int | None = Body(None),
    sell_qty: int | None = Body(None),
    sell_price: int | None = Body(None),
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    update a book
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book_in = await crud.book.get(db, id=id)

    if not book_in or book_in.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    if title is not None:
        book_in.title = title
    if category_id is not None:
        book_in.category_id = category_id
    if borrow_qty is not None:
        book_in.borrow_qty = borrow_qty
    if sell_qty is not None:
        book_in.sell_qty = sell_qty
    if sell_price is not None:
        book_in.sell_price = sell_price

    book = await crud.book.update(
        db,
        db_obj=book_in,
    )
    return APIResponse(book)


@router.delete("/{id}")
async def delete_book(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    delete a book
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book_in = await crud.book.get(db, id=id)

    if not book_in or book_in.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    book = await crud.book.remove(db, id=id)
    return APIResponse(book)
