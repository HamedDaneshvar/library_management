from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    users,
    utils,
    categories,
    books,
    reports,
    sell,
    borrows,
)

api_router = APIRouter()
api_router.include_router(borrows.status_router,
                          prefix="/borrow",)
api_router.include_router(borrows.user_borrow_router,
                          prefix="/borrow",)
api_router.include_router(borrows.staff_borrow_router,
                          prefix="/borrow",)
api_router.include_router(sell.router, prefix="/sell", tags=["sell"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(categories.router,
                          prefix="/categories",
                          tags=["categories"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
