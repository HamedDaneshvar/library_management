from datetime import datetime
from typing import Optional
from pydantic import BaseModel, condecimal


class Status(BaseModel):
    title: str


class StatusCreate(Status):
    pass


class StatusUpdate(Status):
    pass


class Borrow(BaseModel):
    book_id: int
    superuser_id: Optional[int]
    user_id: int
    status_id: int
    start_date: Optional[datetime]
    max_delivery_date: Optional[datetime]
    delivery_date: Optional[datetime]
    borrow_price: Optional[condecimal(max_digits=10, decimal_places=2)]
    borrow_penalty_price: Optional[condecimal(max_digits=10,
                                              decimal_places=2)]
    total_price: Optional[condecimal(max_digits=10, decimal_places=2)]


class BorrowCreate(Borrow):
    pass


class BorrowUpdate(Borrow):
    book_id: Optional[int]
    user_id: Optional[int]


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


class UserPenaltySummary(BaseModel):
    user_id: int
    penalty_count: int
    total_penalty_days: int
