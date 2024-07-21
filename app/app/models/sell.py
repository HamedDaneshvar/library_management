from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Sell(Base):
    __tablename__ = "sells"
    __mapper_args__ = {
        'polymorphic_identity': 'sell',
    }

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    superuser_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    price = Column(Float, nullable=False)

    book = relationship("Book", back_populates="sells")
    superuser = relationship("User", foreign_keys=[superuser_id])
    user = relationship("User", foreign_keys=[user_id])
