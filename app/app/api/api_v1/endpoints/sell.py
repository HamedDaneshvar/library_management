from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


router = APIRouter()
namespace = "sell"


async def find_book(db: AsyncSession, book_id: int) -> models.Book:
    book = await crud.book.get(db, id=book_id)
    if not book or book.is_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def check_book_for_sale(book: models.Book, qty: int):
    if book.sell_qty < qty:
        raise HTTPException(status_code=404,
                            detail="Book is not available for sale")


async def check_user_balance(user: models.User, sell_price: float, qty: int):
    total_price = sell_price * qty
    if user.amount < total_price:
        raise HTTPException(status_code=400,
                            detail="Insufficient account balance")
    return total_price


async def process_sale(
    db: AsyncSession,
    user: models.User,
    book: models.Book,
    qty: int,
    total_price: float
) -> (models.Sell, float):
    # Reduce user balance
    user_in = schemas.UserUpdate(amount=user.amount - total_price)
    await crud.user.update(db, db_obj=user, obj_in=user_in)

    # Reduce book sell quantity
    book_in = schemas.BookUpdate(sell_qty=book.sell_qty - qty)
    await crud.book.update(db, db_obj=book, obj_in=book_in)

    # Create sell record
    sell_obj = schemas.SellCreate(book_id=book.id,
                                  user_id=user.id,
                                  price=total_price)
    sell = await crud.sell.create(db, obj_in=sell_obj)

    # Create payment record
    payment_obj = schemas.PaymentCreate(
        book_id=book.id,
        category_id=book.category_id,
        user_id=user.id,
        model_type=models.Sell.__name__,
        model_id=sell.id,
        price=total_price
    )
    await crud.payment.create(db, obj_in=payment_obj)

    return sell, total_price


@router.get('/book/{book_id}/')
async def sell_book(
    book_id: int,
    qty: int = 1,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
) -> APIResponseType[schemas.SellResponse]:
    """
    Sell book to customer (user with is_superuser=False)
    """
    if current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book = await find_book(db, book_id)
    await check_book_for_sale(book, qty)
    total_price = await check_user_balance(current_user, book.sell_price, qty)
    sell, total_price = await process_sale(db, current_user,
                                           book, qty, total_price)

    message = schemas.SellResponse.generate_message(book.title, qty)

    response = schemas.SellResponse(
        book_name=book.title,
        qty=qty,
        total_price=total_price,
        message=message
    )

    return APIResponse(response)
