from pydantic import BaseModel, condecimal


class Sell(BaseModel):
    book_id: int
    user_id: int
    price: condecimal(max_digits=10, decimal_places=2)

    class Config:
        orm_mode = True


class SellCreate(Sell):
    pass


class SellUpdate(Sell):
    pass


class SellResponse(BaseModel):
    book_name: str
    qty: int
    total_price: condecimal(max_digits=10, decimal_places=2)
    message: str

    @staticmethod
    def generate_message(book_name: str, qty: int) -> str:
        if qty == 1:
            return f"You have successfully bought 1 copy of '{book_name}'"
        return f"You have successfully bought {qty} copies of '{book_name}'"
