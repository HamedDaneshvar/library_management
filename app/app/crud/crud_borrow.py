from datetime import datetime, timedelta
from typing import List
from sqlalchemy import func, desc, asc
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
    UserPenaltySummary,
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

    async def check_category_borrow_limit(
        self, db: AsyncSession, user_id: int, category_id: int
    ) -> bool:
        # Get the borrow limit for the category
        category = await db.execute(
            select(Category).where(Category.id == category_id)
        )
        category_obj = category.scalar_one()
        borrow_limit = category_obj.borrow_limit

        # Count the number of borrowed books in the category by the user
        borrow_count = await db.execute(
            select(func.count(Borrow.id))
            .where(
                Borrow.user_id == user_id,
                Borrow.category_id == category_id,
                Borrow.delivery_date.is_(None),
                Borrow.status_id.in_([5, 6, 7])
            )
        )
        borrow_count = borrow_count.scalar()

        # Check if the borrow count exceeds the borrow limit
        return borrow_count >= borrow_limit

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
                Borrow.status_id.in_([6, 7]),
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

    async def get_borrowed_books_by_user(self, db: AsyncSession, user_id: int):
        subquery = select(Borrow.book_id).where(
            Borrow.user_id == user_id,
            Borrow.status_id.in_([5, 6, 7])
            # 5: Pending, 6: Borrowed, 7: Delivered
        ).subquery()

        query = select(Book).where(Book.id.in_(subquery))

        result = await db.execute(query)
        return result.scalars().all()


class CRUDBorrowActivityLog(CRUDBase[BorrowActivityLog,
                                     BorrowActivityLogCreate,
                                     BorrowActivityLogUpdate]):
    pass


class CRUDUserPenalty(CRUDBase[UserPenalty,
                               UserPenaltyCreate,
                               UserPenaltyUpdate]):
    async def get_user_penalties(
        self, db: AsyncSession, order_by: str = "desc"
    ) -> List[UserPenaltySummary]:
        order_func = desc if order_by == "desc" else asc

        query = (
            select(
                UserPenalty.user_id,
                func.count(UserPenalty.id).label("penalty_count"),
                func.sum(UserPenalty.borrow_penalty_day)
                .label("total_penalty_days"),
            )
            .group_by(UserPenalty.user_id)
            .order_by(order_func("penalty_count"),
                      order_func("total_penalty_days"))
        )

        result = await db.execute(query)
        penalties = result.all()

        return [
            UserPenaltySummary(
                user_id=row[0],
                penalty_count=row[1],
                total_penalty_days=row[2]
            ) for row in penalties
        ]


status = CRUDStatus(Status)
borrow = CRUDBorrow(Borrow)
borrow_activity_log = CRUDBorrowActivityLog(BorrowActivityLog)
user_penalty = CRUDUserPenalty(UserPenalty)
