from pydantic import BaseModel


class Category(BaseModel):
    title: str
    borrow_limit: int
    borrow_price_per_day: float


class CategoryCreate(Category):
    pass


class CategoryUpdate(Category):
    title: str | None
    borrow_limit: int | None
    borrow_price_per_day: float | None
