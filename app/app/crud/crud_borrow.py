from typing import Awaitable, TypeVar
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.borrow import Status
from app.schemas.borrow import StatusCreate, StatusUpdate

from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)


class CRUDStatus(CRUDBase[Status, StatusCreate, StatusUpdate]):
    async def _remove_async(self, db: AsyncSession, *, id: int) -> ModelType:
        db_obj = await self.get(db=db, id=id)
        if db_obj is not None:
            await db.delete(db_obj)
            await db.commit()
            return db_obj
        return None

    def remove(
        self,
        db: Session | AsyncSession,
        *,
        id: int
    ) -> ModelType | Awaitable[ModelType]:
        if isinstance(db, AsyncSession):
            return self._remove_async(db=db, id=id)

        db_obj = db.query(self.model).get(id)
        if db_obj is not None:
            db.delete(db_obj)
            db.commit()
            return db_obj
        return None


status = CRUDStatus(Status)
