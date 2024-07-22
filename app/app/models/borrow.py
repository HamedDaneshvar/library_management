from sqlalchemy import Boolean, Column, Integer, String
from app.db.base_class import Base


class Status(Base):
    __tablename__ = "status"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_deleted = Column(Boolean(), nullable=False, default=False)
