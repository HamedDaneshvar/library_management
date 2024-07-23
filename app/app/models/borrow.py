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

    activity_logs = relationship("BorrowActivityLog", back_populates="status")
    borrow = relationship("Borrow", back_populates="status")


class Borrow(Base):
    __tablename__ = 'borrows'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete="CASCADE"))
    superuser_id = Column(Integer,
                          ForeignKey('user.id', ondelete="SET NULL"),
                          default=None, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    status_id = Column(Integer, ForeignKey('status.id', ondelete="CASCADE"))
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
    penalties = relationship("UserPenalty", back_populates="borrow")
    activity_logs = relationship("BorrowActivityLog", back_populates="borrow")
    status = relationship("Status", foreign_keys=[status_id],
                          back_populates='borrow')


class BorrowActivityLog(Base):
    __tablename__ = 'borrow_activity_log'

    id = Column(Integer, primary_key=True, index=True)
    borrow_id = Column(Integer, ForeignKey('borrows.id', ondelete="CASCADE"))
    status_id = Column(Integer, ForeignKey('status.id', ondelete="CASCADE"))
    is_deleted = Column(Boolean(), default=False)

    borrow = relationship("Borrow", back_populates="activity_logs")
    status = relationship("Status", back_populates="activity_logs")


class UserPenalty(Base):
    __tablename__ = 'user_penalty'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    borrow_id = Column(Integer, ForeignKey('borrows.id', ondelete="CASCADE"))
    borrow_penalty_day = Column(Integer)
    is_deleted = Column(Boolean(), default=False)

    user = relationship("User", back_populates="penalties")
    borrow = relationship("Borrow", back_populates="penalties")
