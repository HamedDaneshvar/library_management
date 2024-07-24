from celery import Celery
from app.core.celery_app import celery_app
from app import crud
from app.api import deps


@celery_app.task(name="app.celery.tasks.deduct_book_cost")
def deduct_book_cost():
    try:
        # Get the database session generator
        db_generator = deps.get_db()
        # Get the first value from the generator (this yields the session)
        db = next(db_generator)

        try:
            # Retrieve all users
            users = crud.user.get_multi(db)
            for user in users:
                # Retrieve active borrows for each user
                borrows = crud.borrow.get_active_borrows_by_user(db, user.id)
                for borrow in borrows:
                    # Retrieve book category
                    category = crud.category.get(db,
                                                 id=borrow.book.category_id)
                    cost = category.borrow_price_per_day
                    # Deduct cost from user's amount
                    user.amount -= cost
                    # Commit the changes
                    db.commit()
            print("Book costs deducted successfully.")
        finally:
            # Close the session
            db.close()
            # Clean up the generator
            db_generator.close()
    except Exception as e:
        print(f"Error in deduct_book_cost task: {e}")
