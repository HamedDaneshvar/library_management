from sqlalchemy import Boolean, Column, Integer, Numeric, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    amount = Column(Numeric(10, 2), nullable=False, default=0.0)
    is_deleted = Column(Boolean(), nullable=False, default=False)

    sells = relationship('Sell', foreign_keys='Sell.user_id',
                         back_populates='user')
    payments = relationship('Payment', back_populates='user')
    borrows_user = relationship('Borrow', foreign_keys='Borrow.user_id',
                                back_populates='user')
    borrows_superuser = relationship(
        'Borrow',
        foreign_keys='Borrow.superuser_id',
        back_populates='superuser'
    )
    penalties = relationship('UserPenalty', back_populates='user')
