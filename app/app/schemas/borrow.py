from datetime import datetime
from pydantic import BaseModel


class Status(BaseModel):
    title: str


class StatusCreate(Status):
    pass


class StatusUpdate(Status):
    pass


class Borrow(BaseModel):
    book_id: int
    superuser_id: int
    user_id: int
    start_date: datetime
    max_delivery_date: datetime
    delivery_date: datetime
    borrow_price: float
    borrow_penalty_price: float
    total_price: float


class BorrowCreate(Borrow):
    pass


class Borrowupdate(Borrow):
    pass


class BorrowActivityLog(BaseModel):
    borrow_id: int
    status_id: int


class BorrowActivityLogCreate(BorrowActivityLog):
    pass


class BorrowActivityLogUpdate(BorrowActivityLog):
    pass


class UserPenalty(BaseModel):
    user_id: int
    borrow_id: int 
    borrow_penalty_day: int


class UserPenaltyCreate(UserPenalty):
    pass


class UserPenaltyUpdate(UserPenalty):
    pass
