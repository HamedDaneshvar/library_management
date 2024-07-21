from pydantic import BaseModel


class Book(BaseModel):
    title: str
    category_id: int
    borrow_qty: int
    sell_qty: int
    sell_price: int


class BookCreate(Book):
    pass


class BookUpdate(Book):
    pass
