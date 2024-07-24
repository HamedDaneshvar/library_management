from sqlalchemy import Boolean, Column, Numeric, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    borrow_qty = Column(Integer, nullable=False, default=0)
    sell_qty = Column(Integer, nullable=False, default=0)
    sell_price = Column(Numeric(10, 2), nullable=False)
    is_deleted = Column(Boolean(), nullable=False, default=False)

    category = relationship('Category', back_populates='books')
    sells = relationship('Sell', back_populates='book')
    payments = relationship('Payment', back_populates='book')
    borrows = relationship('Borrow', back_populates='book')
