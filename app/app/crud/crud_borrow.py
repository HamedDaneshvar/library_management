from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.borrow import Status, Borrow, BorrowActivityLog, UserPenalty
from app.schemas.borrow import (
    StatusCreate,
    StatusUpdate,
    BorrowCreate,
    BorrowUpdate,
    BorrowActivityLogCreate,
    BorrowActivityLogUpdate,
    UserPenaltyCreate,
    UserPenaltyUpdate,
)
from app.models import Category, Book, User


class CRUDStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    pass


class CRUDBorrow(CRUDBase[Borrow, BorrowCreate, BorrowUpdate]):
    async def _has_pending_borrows_async(
            self,
            db: AsyncSession,
            query
    ) -> bool:
        result = await db.scalar(query)
        return result > 0

    def has_pending_borrows(
            self,
            db: Session | AsyncSession,
            user_id: int
    ) -> bool:
        query = (
            select(func.count())
            .select_from(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.max_delivery_date <= datetime.now(),
                self.model.delivery_date == None
            )
        )

        if isinstance(db, AsyncSession):
            return self._has_pending_borrows_async(db, query)
        return db.scalar(query) > 0

    async def user_has_not_enough_balance(
            self,
            db: AsyncSession,
            user_id: int,
            category_id: int
    ) -> bool:
        # Query to get the borrow price per day from the book's category
        query = (
            select(Category.borrow_price_per_day, User.amount)
            .join(User, User.id == user_id)
            .where(Category.id == category_id)
        )

        result = await db.execute(query)
        category_price_per_day, user_amount = result.first()

        # Calculate the cost for 3 days
        cost_for_three_days = category_price_per_day * 3

        # Check if user has enough balance
        return user_amount <= cost_for_three_days

    async def get_borrow_days(
            self,
            db: AsyncSession,
            book_id: int,
            borrow_qty: int,
            requested_days: int
    ) -> int:
        # Calculate f(30)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        f_30_query = (
            select(func.count())
            .select_from(Borrow)
            .where(  # status_id -> Borrowed, Delivered
                Borrow.book_id == book_id,
                Borrow.status_id.in_([4, 5]),
                Borrow.start_date >= thirty_days_ago
            )
        )
        f_30_result = await db.execute(f_30_query)
        f_30 = f_30_result.scalar()

        # Apply the formula
        calculated_days = int((30 * borrow_qty) / (borrow_qty + f_30)) + 1

        # Determine the number of days to return
        if calculated_days < 3:
            return 3
        return min(requested_days, calculated_days)

    async def update_and_calculate_borrow(
        self, db: AsyncSession,
        status_id: int,
        superuser_id: int,
        borrow: Borrow
    ) -> Borrow:
        # Fetch category details
        category = await db.get(Category, borrow.category_id)

        # Calculate borrow price
        days_borrowed = (borrow.max_delivery_date - borrow.start_date).days
        borrow_price = days_borrowed * category.borrow_price_per_day

        # Calculate borrow penalty price
        now = datetime.now()
        days_penalty = (now - borrow.max_delivery_date).days \
            if now > borrow.max_delivery_date else 0
        borrow_penalty_price = days_penalty * category.borrow_price_per_day

        # Calculate total price
        total_price = borrow_price + borrow_penalty_price

        # Update borrow object
        borrow.delivery_date = now
        borrow.status_id = status_id
        borrow.superuser_id = superuser_id
        borrow.borrow_price = borrow_price
        borrow.borrow_penalty_price = borrow_penalty_price
        borrow.total_price = total_price

        return await self.update(db, db_obj=borrow, obj_in=borrow)


class CRUDBorrowActivityLog(CRUDBase[BorrowActivityLog,
                                     BorrowActivityLogCreate,
                                     BorrowActivityLogUpdate]):
    pass


class CRUDUserPenalty(CRUDBase[UserPenalty,
                               UserPenaltyCreate,
                               UserPenaltyUpdate]):
    pass


status = CRUDStatus(Status)
borrow = CRUDBorrow(Borrow)
borrow_activity_log = CRUDBorrowActivityLog(BorrowActivityLog)
user_penalty = CRUDUserPenalty(UserPenalty)
