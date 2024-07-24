from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import APIResponseType, APIResponse
from app import crud, models, schemas


status_router = APIRouter(prefix="/status", tags=["borrow status"])
user_borrow_router = APIRouter(prefix="/user", tags=["user borrow"])
staff_borrow_router = APIRouter(prefix="/staff", tags=["staff borrow"])
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
async def borrow_book_request(
    book_id: int,
    requested_days: Optional[int] = None,
    db: AsyncSession = Depends(deps.get_db_async),
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Request to borrow a book
    """

    if current_user.is_superuser:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    book = await find_book(db, book_id)

    user_id = current_user.id

    # step 1: insert this request into borrow table and activity log
    status_id = 1  # Requested
    borrow_obj = schemas.BorrowCreate(
        book_id=book.id,
        user_id=user_id,
        status_id=1
    )
    # create borrow request
    borrow = await crud.borrow.create(db, obj_in=borrow_obj)
    await create_activity_log(db, borrow.id, status_id)

    await check_book_for_borrow(book)

    rejected_message = []

    # step 2: maximum possible number of books from this category
    status_id = 2
    category_borrow_limit = await crud.borrow.check_category_borrow_limit(
        db, user_id, book.category_id)
    if category_borrow_limit:
        # update borrow record
        status_message = await crud.status.get(db, id=status_id)
        borrow_update = schemas.BorrowUpdate(
            status_id=status_id
        )
        borrow = await crud.borrow.update(db, db_obj=borrow,
                                          obj_in=borrow_update)
        # create new activity log record
        await create_activity_log(db, borrow.id, status_id)
        rejected_message.append(status_message.title)

    # step 3: if user has pending borrows is rejected
    status_id = 3
    has_pending = await crud.borrow.has_pending_borrows(db, user_id)
    if has_pending:
        # update borrow record
        status_message = await crud.status.get(db, id=status_id)
        borrow_update = schemas.BorrowUpdate(
            status_id=status_id
        )
        borrow = await crud.borrow.update(db, db_obj=borrow,
                                          obj_in=borrow_update)
        # create new activity log record
        await create_activity_log(db, borrow.id, status_id)
        rejected_message.append(status_message.title)

    # step 4: Checking the balance of the user who has enough balance
    # to borrow this book for 3 days
    status_id = 4
    category_id = book.category_id
    has_not_enough_balance = await crud.borrow.user_has_not_enough_balance(
                            db, user_id, category_id)
    if has_not_enough_balance:
        # update borrow record
        status_message = await crud.status.get(db, id=status_id)
        borrow_update = schemas.BorrowUpdate(
            status_id=status_id
        )
        borrow = await crud.borrow.update(db, db_obj=borrow,
                                          obj_in=borrow_update)
        # create new activity log record
        await create_activity_log(db, borrow.id, status_id)
        rejected_message.append(status_message.title)

    # step 5: display to user why his/her is reject
    if has_pending or has_not_enough_balance:
        raise HTTPException(status_code=400, detail=rejected_message)

    # step 6: Calculate the number of days the user can borrow the book
    status_id = 5  # pending
    borrow_days = await crud.borrow.get_borrow_days(
        db, book_id, book.borrow_qty, requested_days or 3)

    borrow_update = schemas.BorrowUpdate(
        status_id=status_id,
        start_date=datetime.now(),
        max_delivery_date=datetime.now() + timedelta(days=borrow_days)
    )
    borrow = await crud.borrow.update(db, db_obj=borrow,
                                      obj_in=borrow_update)
    # create new activity log record
    await create_activity_log(db, borrow.id, status_id)

    # step 7: Reduce the number of books to borrow
    book_update = schemas.BookUpdate(
        borrow_qty=book.borrow_qty - 1
    )
    book = await crud.book.update(db, db_obj=book,
                                  obj_in=book_update)

    return APIResponse({"message": "Your requested book has been reserved,\
                         please pick up the desired book from the \
                        library staff",
                        "borrow_days": borrow_days})


@staff_borrow_router.put("/lending-book")
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


@staff_borrow_router.put("/delivered-book")
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

    # Insert the borrowing transaction in the payments model
    payment_create = schemas.PaymentCreate(
        book_id=borrow.book_id,
        category_id=borrow.category_id,
        user_id=borrow.user_id,
        model_type=models.Borrow.__name__,
        model_id=borrow.id,
        price=borrow.total_price
    )
    payment = await crud.payment.create(db, obj_in=payment_create)

    return APIResponse({"message": "Book was lent to the user"})
