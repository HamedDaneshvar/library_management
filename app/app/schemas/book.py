from pydantic import BaseModel


class Book(BaseModel):
    title: str
    category_id: int
    borrow_qty: int
    sell_qty: int
    sell_price: int

    class Config:
        orm_mode = True


class BookCreate(Book):
    pass


class BookUpdate(Book):
    title: str | None
    category_id: int | None
    borrow_qty: int | None
    sell_qty: int | None
    sell_price: int | None
