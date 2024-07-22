from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_deleted = Column(Boolean(), nullable=False, default=False)


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"))
    superuser_id = Column(Integer,
                          ForeignKey('user.id', ondelete="SET NULL"),
                          default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    start_date = Column(DateTime, default=None, nullable=True)
    max_delivery_date = Column(DateTime, default=None, nullable=True)
    delivery_date = Column(DateTime, default=None, nullable=True)
    borrow_price = Column(Float, nullable=True)
    borrow_penalty_price = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)
    is_deleted = Column(Boolean(), default=False)

    book = relationship("Book", back_populates="borrows")
    superuser = relationship("User", foreign_keys=[superuser_id],
                             back_populates='borrows_superuser')
    user = relationship("User", foreign_keys=[user_id],
                        back_populates='borrows_user')
    user_penalty = relationship("UserPenalty", back_populates="user_penalty")


class BorrowActivityLog(Base):
    __tablename__ = 'borrow_activity_log'

    id = Column(Integer, primary_key=True, index=True)
    borrow_id = Column(Integer, ForeignKey('borrows.id', ondelete="CASCADE"))
    status_id = Column(Integer, ForeignKey('status.id', ondelete="CASCADE"))
    is_deleted = Column(Boolean(), default=False)

    borrow = relationship("Borrow", foreign_keys=[borrow_id])
    status = relationship("Status", foreign_keys=[status_id])


class UserPenalty(Base):
    __tablename__ = 'user_penalty'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    borrow_id = Column(Integer, ForeignKey('borrows.id', ondelete="CASCADE"))
    borrow_penalty_day = Column(Integer)
    is_deleted = Column(Boolean(), default=False)

    user = relationship("User", foreign_keys=[user_id])
    borrow = relationship("Borrow", foreign_keys=[borrow_id])
