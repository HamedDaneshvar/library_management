from fastapi import APIRouter

from app.api.api_v1.endpoints import users, utils, categories

api_router = APIRouter()
api_router.include_router(categories.router,
                          prefix="/categories",
                          tags=["categories"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
