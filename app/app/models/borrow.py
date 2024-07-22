from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Status(Base):
    __tablename__ = "Status"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
