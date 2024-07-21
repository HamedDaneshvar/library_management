from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, polymorphic_identity, polymorphic_relationship
from app.db.base_class import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    model_type = Column(String, nullable=False)
    model_id = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    book = relationship("Book", back_populates="payments")
    category = relationship("Category", foreign_keys=[category_id])
    user = relationship("User", foreign_keys=[user_id])

    # Polymorphic relationships
    model = polymorphic_relationship(model_type)
