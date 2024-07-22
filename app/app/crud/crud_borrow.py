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
    pass


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
