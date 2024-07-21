from pydantic import BaseModel


class Category(BaseModel):
    title: str
    borrow_limit: int
    borrow_price_per_day: int


class CategoryCreate(Category):
    pass


class CategoryUpdate(Category):
    pass
