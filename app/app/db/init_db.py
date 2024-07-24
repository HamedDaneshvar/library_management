import logging
import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
    # Create 3 Users
    users = [
        models.User(full_name="Alice Johnson", email="alice@example.com",
                    hashed_password=get_password_hash("hashedpassword1"),
                    amount=100.0),
        models.User(full_name="Bob Smith", email="bob@example.com",
                    hashed_password=get_password_hash("hashedpassword2"),
                    amount=150.0),
        models.User(full_name="Charlie Brown", email="charlie@example.com",
                    hashed_password=get_password_hash("hashedpassword3"),
                    amount=200.0),
        models.User(full_name="Test User", email="testuser@example.com",
                    hashed_password=get_password_hash("hashed_password"),
                    amount=100.0)
    ]
    db.add_all(users)
    db.commit()

    # Create 7 Status
    statuses = ["Requested",
                "Rejected because you borrowed the maximum possible "
                "number of books from this category",
                "Rejected for not delivering the borrowed book",
                "Rejected because your account balance is not enough "
                "to borrow a book for 3 days",
                "Pending",
                "Borrowed",
                "Delivered"]
    for title in statuses:
        status = models.Status(title=title)
        db.add(status)

    db.commit()

    # Fetch user IDs and status IDs
    user_ids = [user.id for user in
                (db.execute(select(models.User))).scalars().all()]
    status_ids = [status.id for status in
                  (db.execute(select(models.Status))).scalars().all()]

    # Add initial sells
    sells = [
        models.Sell(book_id=1, user_id=random.choice(user_ids), price=15.99),
        models.Sell(book_id=3, user_id=random.choice(user_ids), price=20.00),
        models.Sell(book_id=5, user_id=random.choice(user_ids), price=18.75),
        models.Sell(book_id=7, user_id=random.choice(user_ids), price=30.99),
        models.Sell(book_id=9, user_id=random.choice(user_ids), price=35.99),
    ]
    db.add_all(sells)
    db.commit()

    # Create 15 Payments
    model_type = [models.Sell.__name__, models.Borrow.__name__]
    for i in range(15):
        payment = models.Payment(
            book_id=random.randint(1, 10),
            category_id=random.randint(1, 5),
            user_id=random.choice(user_ids),
            model_type=random.choice(model_type),
            model_id=random.randint(1, 30),
            price=random.uniform(10, 100)
        )
        db.add(payment)

    db.commit()

    # Create 30 Borrows
    for i in range(30):
        start_date = datetime.now() - timedelta(days=random.randint(1, 30))
        max_delivery_date = start_date + timedelta(days=14)
        delivery_date = max_delivery_date + timedelta(
            days=random.randint(0, 10)) if random.random() < 0.5 else None
        borrow = models.Borrow(
            book_id=random.randint(1, 20),
            user_id=random.choice(user_ids),
            status_id=random.choice(status_ids),
            start_date=start_date,
            max_delivery_date=max_delivery_date,
            delivery_date=delivery_date,
            borrow_price=random.uniform(5, 20),
            borrow_penalty_price=random.uniform(0, 10) if delivery_date else 0,
            total_price=random.uniform(10, 30)
        )
        db.add(borrow)

    # Create 10 Borrows for test celery task
    for i in range(10):
        start_date = datetime.now() - timedelta(days=random.randint(1, 30))
        max_delivery_date = start_date + timedelta(days=14)
        delivery_date = None
        borrow = models.Borrow(
            book_id=random.randint(1, 20),
            user_id=random.choice(user_ids),
            status_id=random.choice([5, 6, 7]),
            start_date=start_date,
            max_delivery_date=max_delivery_date,
            delivery_date=delivery_date,
            borrow_price=random.uniform(5, 20),
            borrow_penalty_price=random.uniform(0, 10) if delivery_date else 0,
            total_price=random.uniform(10, 30)
        )
        db.add(borrow)

    db.commit()

    # Create 30 Borrow Activity Logs
    borrow_ids = [borrow.id for borrow in
                  (db.execute(select(models.Borrow))).scalars().all()]
    for i in range(30):
        activity_log = models.BorrowActivityLog(
            borrow_id=random.choice(borrow_ids),
            status_id=random.choice(status_ids)
        )
        db.add(activity_log)

    db.commit()

    # Create 15 User Penalties
    for i in range(15):
        user_penalty = models.UserPenalty(
            user_id=random.choice(user_ids),
            borrow_id=random.choice(borrow_ids),
            borrow_penalty_day=random.randint(1, 10)
        )
        db.add(user_penalty)

    db.commit()


def init_db(db: Session) -> None:
    create_super_admin(db)
    create_initial_data(db)


if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
