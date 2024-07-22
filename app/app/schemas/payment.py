from pydantic import BaseModel


class Payment(BaseModel):
    book_id: int
    category_id: int
    user_id: int
    model_type: str
    model_id: int
    price: float

    class Config:
        orm_mode = True


class PaymentCreate(Payment):
    pass


class PaymentUpdate(Payment):
    pass


class RevenueSummary(BaseModel):
    category_id: int
    total_price: float
