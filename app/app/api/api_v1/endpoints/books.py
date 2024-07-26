from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Body
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


router = APIRouter()
namespace = "book"


def map_books_to_schema(
    user: models.User,
    books: List[models.Book]
) -> Union[List[schemas.BookOutSuperuser] | List[schemas.BookOutUser]]:
    if user.is_superuser:
        return [schemas.BookOutSuperuser(
                title=book.title,
                category=book.category,
                borrow_qty=book.borrow_qty,
                sell_qty=book.sell_qty,
                sell_price=book.sell_price,)
                for book in books]
    else:
        return [schemas.BookOutUser(
                title=book.title,
                category=book.category)
                for book in books]


@router.get("/")
async def get_books(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[Union[List[schemas.BookOutSuperuser] |
                           List[schemas.BookOutUser]]]:
    """
    Retrieve books.
    """
    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=401, detail="Unauthorized access")

    books = await crud.book.filter(
        db,
        skip=skip,
        limit=limit,
        is_deleted=False
    )
    books = map_books_to_schema(current_user, books)
    return APIResponse(books)


@router.get("/{id}/")
async def get_book(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[Union[schemas.BookOutSuperuser |
                           schemas.BookOutUser]]:
    """
    Retrieve a book.
    """
    # if not current_user.is_superuser:
    #     raise HTTPException(status_code=401, detail="Unauthorized access")

    book = await crud.book.get(db, id=id)
    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    book = map_books_to_schema(current_user, [book])[0]
    return APIResponse(book)


@router.post("/")
async def create_book(
    book_in: schemas.BookCreate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[schemas.BookOutSuperuser]:
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
    book = map_books_to_schema(current_user, [book])[0]
    return APIResponse(book)


@router.put("/{id}/")
async def update_book(
    id: int,
    request: schemas.BookUpdate,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[schemas.BookOutSuperuser]:
    """
    update a book
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book_in = await crud.book.get(db, id=id)

    if not book_in or book_in.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    if request.title is not None:
        book_in.title = request.title
    if request.category_id is not None:
        book_in.category_id = request.category_id
    if request.borrow_qty is not None:
        book_in.borrow_qty = request.borrow_qty
    if request.sell_qty is not None:
        book_in.sell_qty = request.sell_qty
    if request.sell_price is not None:
        book_in.sell_price = request.sell_price

    book = await crud.book.update(
        db,
        db_obj=book_in,
    )
    book = map_books_to_schema(current_user, [book])[0]
    return APIResponse(book)


@router.delete("/{id}/")
async def delete_book(
    id: int,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[schemas.BookDelete]:
    """
    delete a book
    """

    if not current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book_in = await crud.book.get(db, id=id)

    if not book_in or book_in.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")

    book = await crud.book.remove(db, id=id)
    item = schemas.BookDelete()
    return APIResponse(item)
