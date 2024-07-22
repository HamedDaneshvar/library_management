import logging

from sqlalchemy.orm import Session

from app import models
from app.core.config import settings
from app.core.security import get_password_hash
from app.db import base  # noqa: F401
from app.db.session import SessionLocal

logger = logging.getLogger(__name__)


def create_super_admin(db: Session) -> None:
    user = (
        db.query(models.User)
        .filter(models.User.email == settings.FIRST_SUPERUSER)
        .first()
    )

    if not user:
        user = models.User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(
                settings.FIRST_SUPERUSER_PASSWORD
            ),
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)


def create_initial_data(db: Session) -> None:
    # Add initial categories
    categories = [
        models.Category(title="Fiction", borrow_limit=5,
                        borrow_price_per_day=1.5),
        models.Category(title="Science", borrow_limit=3,
                        borrow_price_per_day=2.0),
        models.Category(title="History", borrow_limit=4,
                        borrow_price_per_day=1.0),
        models.Category(title="Technology", borrow_limit=6,
                        borrow_price_per_day=2.5),
        models.Category(title="Arts", borrow_limit=2,
                        borrow_price_per_day=3.0),
    ]
    db.add_all(categories)
    db.commit()

    # Add initial books
    books = [
        models.Book(title="Book 1", category_id=1,
                    borrow_qty=10, sell_qty=5, sell_price=15.99),
        models.Book(title="Book 2", category_id=1,
                    borrow_qty=8, sell_qty=4, sell_price=12.99),
        models.Book(title="Book 3", category_id=2,
                    borrow_qty=7, sell_qty=3, sell_price=20.00),
        models.Book(title="Book 4", category_id=2,
                    borrow_qty=5, sell_qty=5, sell_price=22.50),
        models.Book(title="Book 5", category_id=3,
                    borrow_qty=6, sell_qty=6, sell_price=18.75),
        models.Book(title="Book 6", category_id=3,
                    borrow_qty=4, sell_qty=2, sell_price=25.00),
        models.Book(title="Book 7", category_id=4,
                    borrow_qty=12, sell_qty=8, sell_price=30.99),
        models.Book(title="Book 8", category_id=4,
                    borrow_qty=9, sell_qty=7, sell_price=27.50),
        models.Book(title="Book 9", category_id=5,
                    borrow_qty=11, sell_qty=9, sell_price=35.99),
        models.Book(title="Book 10", category_id=5,
                    borrow_qty=10, sell_qty=5, sell_price=40.00),
        models.Book(title="Book 11", category_id=1,
                    borrow_qty=8, sell_qty=4, sell_price=12.99),
        models.Book(title="Book 12", category_id=1,
                    borrow_qty=7, sell_qty=3, sell_price=15.99),
        models.Book(title="Book 13", category_id=2,
                    borrow_qty=10, sell_qty=5, sell_price=18.50),
        models.Book(title="Book 14", category_id=2,
                    borrow_qty=5, sell_qty=5, sell_price=22.99),
        models.Book(title="Book 15", category_id=3,
                    borrow_qty=6, sell_qty=4, sell_price=16.75),
        models.Book(title="Book 16", category_id=3,
                    borrow_qty=4, sell_qty=3, sell_price=20.00),
        models.Book(title="Book 17", category_id=4,
                    borrow_qty=11, sell_qty=8, sell_price=28.50),
        models.Book(title="Book 18", category_id=4,
                    borrow_qty=9, sell_qty=6, sell_price=24.99),
        models.Book(title="Book 19", category_id=5,
                    borrow_qty=12, sell_qty=7, sell_price=32.00),
        models.Book(title="Book 20", category_id=5,
                    borrow_qty=10, sell_qty=5, sell_price=38.75),
    ]
    db.add_all(books)
    db.commit()

    # Add a user for testing
    user = models.User(full_name="Test User", email="testuser@example.com",
                       hashed_password=get_password_hash("hashed_password"),
                       amount=100.0)
    db.add(user)
    db.commit()

    # Add initial sells
    sells = [
        models.Sell(book_id=1, user_id=2, price=15.99),
        models.Sell(book_id=3, user_id=2, price=20.00),
        models.Sell(book_id=5, user_id=2, price=18.75),
        models.Sell(book_id=7, user_id=2, price=30.99),
        models.Sell(book_id=9, user_id=2, price=35.99),
    ]
    db.add_all(sells)
    db.commit()

    # Add initial payments
    payments = [
        models.Payment(book_id=1, category_id=1, user_id=2,
                       model_type="Sell", model_id=1, price=15.99),
        models.Payment(book_id=3, category_id=2, user_id=2,
                       model_type="Sell", model_id=2, price=20.00),
        models.Payment(book_id=5, category_id=3, user_id=2,
                       model_type="Sell", model_id=3, price=18.75),
        models.Payment(book_id=7, category_id=4, user_id=2,
                       model_type="Sell", model_id=4, price=30.99),
        models.Payment(book_id=9, category_id=5, user_id=2,
                       model_type="Sell", model_id=5, price=35.99),
    ]
    db.add_all(payments)
    db.commit()


def init_db(db: Session) -> None:
    create_super_admin(db)
    create_initial_data(db)


if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
