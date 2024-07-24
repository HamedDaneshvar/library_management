from pydantic import BaseModel, condecimal


class Book(BaseModel):
    title: str
    category_id: int
    borrow_qty: int
    sell_qty: int
    sell_price: condecimal(max_digits=10, decimal_places=2)

    class Config:
        orm_mode = True


class BookCreate(Book):
    pass


class BookUpdate(Book):
    title: str | None
    category_id: int | None
    borrow_qty: int | None
    sell_qty: int | None
    sell_price: condecimal(max_digits=10, decimal_places=2) | None


class BookOutUser(BaseModel):
    title: str
    category_id: int


class BookOutSuperuser(Book):
    pass


class BookDelete(BaseModel):
    message: str = "Book item deleted successfully"
