from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .book import Book


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    borrow_limit = Column(Integer, nullable=False)
    borrow_price_per_day = Column(Integer, nullable=False)

    books = relationship(Book, back_populates="category")
