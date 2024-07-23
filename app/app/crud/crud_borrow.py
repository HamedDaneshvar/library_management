from datetime import datetime

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
