from sqlalchemy import Boolean, Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Sell(Base):
    __tablename__ = "sells"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_deleted = Column(Boolean(), nullable=False, default=False)

    book = relationship("Book", back_populates="sells")
    user = relationship("User", foreign_keys=[user_id])
