from sqlalchemy import Boolean, Column, Numeric, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false
from app.db.base_class import Base
from app.models.book import Book


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    borrow_limit = Column(Integer, nullable=False)
    borrow_price_per_day = Column(Numeric(10, 2), nullable=False)
    is_deleted = Column(Boolean(), nullable=False, default=False)

    books = relationship('Book', back_populates="category")
