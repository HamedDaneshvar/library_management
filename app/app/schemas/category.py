from pydantic import BaseModel, condecimal


class Category(BaseModel):
    title: str
    borrow_limit: int
    borrow_price_per_day: condecimal(max_digits=10, decimal_places=2)


class CategoryCreate(Category):
    pass


class CategoryUpdate(Category):
    title: str | None
    borrow_limit: int | None
    borrow_price_per_day: condecimal(max_digits=10, decimal_places=2) | None


class CategoryOut(Category):
    class Config:
        orm_mode = True


class CategoryOutUser(BaseModel):
    title: str
    borrow_price_per_day: condecimal(max_digits=10, decimal_places=2)

    class Config:
        orm_mode = True


class CategoryOutSuperuser(Category):
    class Config:
        orm_mode = True


class CategoryDelete(BaseModel):
    message: str = "Item deleted successfully"
