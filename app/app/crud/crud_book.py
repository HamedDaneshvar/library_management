from typing import Any, List, Union, Awaitable
from sqlalchemy.future import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class CRUDBook(CRUDBase[Book, BookCreate, BookUpdate]):
    def get(
        self, db: Session | AsyncSession, id: Any
    ) -> Book | Awaitable[Book] | None:
        query = select(self.model).options(selectinload(Book.category))\
            .filter(self.model.id == id)
        return self._first(db.scalars(query))

    async def _filter_async(
        self,
        db: AsyncSession,
        *args,
        skip: int = None,
        limit: int = None,
        **kwargs
    ) -> List[Book]:
        query = select(self.model).options(selectinload(Book.category))\
            .filter(*args).filter_by(**kwargs)

        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)

        return await self._all(db.scalars(query))

    def filter(
        self,
        db: Union[Session, AsyncSession],
        *args,
        skip: int = None,
        limit: int = None,
        **kwargs
    ) -> Union[List[Book], Awaitable[List[Book]]]:
        query = select(self.model).options(selectinload(Book.category))\
            .filter(*args).filter_by(**kwargs)

        if skip is not None:
            query = query.offset(skip)
        if limit is not None:
            query = query.limit(limit)

        if isinstance(db, AsyncSession):
            return self._filter_async(db, *args, skip=skip,
                                      limit=limit, **kwargs)
        return self._all(db.scalars(query))


book = CRUDBook(Book)
